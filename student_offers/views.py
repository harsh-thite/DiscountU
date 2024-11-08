from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Category, Discount, UserBookmark, UserProfile, DiscountClick
from .forms import DiscountSearchForm, DiscountSubmissionForm, CustomAuthenticationForm, CustomUserCreationForm, UserProfileForm

class AuthMixin:
    """Mixin for authentication-related functionality"""

    def handle_successful_login(self, request, user, redirect_url='home'):
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect(redirect_url)


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                return AuthMixin().handle_successful_login(request, user, next_url)

        messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
        'next': next_url
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            # Create user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Save selected interests
            interests = profile_form.cleaned_data.get('interests', [])
            profile.interests.set(interests)

            login(request, user)
            messages.success(request, "Registration successful! Complete your profile to get personalized discounts.")
            return redirect('complete_profile')
    else:
        form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {
        'form': form,
        'profile_form': profile_form
    })


@login_required
def dashboard_view(request):
    # Get user's bookmarked discounts
    bookmarked_discounts = Discount.objects.filter(
        bookmarks__user=request.user
    ).select_related('category')

    # Get recommended discounts based on user's interests
    user_interests = request.user.userprofile.interests.all()
    recommended_discounts = Discount.objects.filter(
        category__in=user_interests,
        status='active',
        valid_until__gt=timezone.now()
    ).exclude(
        bookmarks__user=request.user
    ).order_by('-created_at')[:5]

    # Get recently viewed discounts
    recent_views = DiscountClick.objects.filter(
        user=request.user
    ).select_related('discount').order_by('-clicked_at')[:5]

    context = {
        'bookmarked_discounts': bookmarked_discounts,
        'recommended_discounts': recommended_discounts,
        'recent_views': recent_views,
    }
    return render(request, 'dashboard.html', context)


def discount_list(request):
    discounts = Discount.objects.filter(
        status='active',
        valid_until__gt=timezone.now()
    ).select_related('category')

    form = DiscountSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        sort_by = form.cleaned_data.get('sort_by')

        if search_query:
            discounts = discounts.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(company_name__icontains=search_query)
            )

        if category:
            discounts = discounts.filter(category=category)

        if sort_by == 'newest':
            discounts = discounts.order_by('-created_at')
        elif sort_by == 'popular':
            discounts = discounts.annotate(
                bookmark_count=Count('bookmarks')
            ).order_by('-bookmark_count')
        elif sort_by == 'ending_soon':
            discounts = discounts.order_by('valid_until')

    paginator = Paginator(discounts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'discount_list.html', {
        'form': form,
        'page_obj': page_obj,
        'total_count': paginator.count
    })


def category_list(request):
    categories = Category.objects.filter(
        is_active=True
    ).annotate(
        discount_count=Count('discounts', filter=Q(
            discounts__status='active',
            discounts__valid_until__gt=timezone.now()
        ))
    ).order_by('order', 'name')

    return render(request, 'category_listing.html', {
        'categories': categories
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)

    discounts = category.discounts.filter(
        status='active',
        valid_until__gt=timezone.now()
    ).select_related('category')

    # Get user's bookmarked discounts if authenticated
    bookmarked_discounts = set()
    if request.user.is_authenticated:
        bookmarked_discounts = set(
            UserBookmark.objects.filter(
                user=request.user,
                discount__in=discounts
            ).values_list('discount_id', flat=True)
        )

    paginator = Paginator(discounts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'category_detail.html', {
        'category': category,
        'page_obj': page_obj,
        'bookmarked_discounts': bookmarked_discounts
    })


@login_required
@require_http_methods(["POST"])
def toggle_bookmark(request, discount_id):
    try:
        discount = get_object_or_404(Discount, id=discount_id)
        bookmark, created = UserBookmark.objects.get_or_create(
            user=request.user,
            discount=discount
        )

        if not created:
            bookmark.delete()
            discount.saves_count = F('saves_count') - 1
        else:
            discount.saves_count = F('saves_count') + 1

        discount.save()

        return JsonResponse({
            'status': 'created' if created else 'removed',
            'saves_count': discount.saves_count
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
def track_discount_click(request, discount_id):
    try:
        discount = get_object_or_404(Discount, id=discount_id)

        # Record the click
        DiscountClick.objects.create(
            discount=discount,
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        # Update click count
        discount.clicks_count = F('clicks_count') + 1
        discount.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            instance=request.user.userprofile
        )
        if form.is_valid():
            profile = form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'profile.html', {'form': form})


def submit_discount(request):
    if request.method == 'POST':
        form = DiscountSubmissionForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.status = 'coming_soon'
            discount.save()
            messages.success(request, "Thank you for submitting your discount. It will be reviewed and published soon.")
            return redirect('home')
    else:
        form = DiscountSubmissionForm()
    return render(request, 'submit_discount.html', {'form': form})