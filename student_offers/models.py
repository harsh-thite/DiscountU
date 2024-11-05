from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Icon name from Lucide icons")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order on the site")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']


class Discount(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('coming_soon', 'Coming Soon'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    website_url = models.URLField()
    company_name = models.CharField(max_length=100)
    company_logo = models.URLField(blank=True, null=True, help_text="URL to company logo")

    # Discount details
    discount_type = models.CharField(max_length=20, choices=[
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('special', 'Special Offer')
    ])
    discount_percentage = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    # Categories and tags
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='discounts'
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated tags"
    )

    # Redemption details
    requirements = models.TextField(help_text="What students need to get this discount")
    how_to_redeem = models.TextField(help_text="Steps to redeem the discount")
    promo_code = models.CharField(max_length=50, blank=True)

    # Validity
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Metrics
    views_count = models.PositiveIntegerField(default=0)
    clicks_count = models.PositiveIntegerField(default=0)
    saves_count = models.PositiveIntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_discounts'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.company_name}-{self.title}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('discount_detail', kwargs={'slug': self.slug})

    def is_valid(self):
        now = timezone.now()
        if self.valid_until:
            return self.valid_from <= now <= self.valid_until
        return self.valid_from <= now

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return f"{self.company_name} - {self.title}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'valid_from', 'valid_until']),
            models.Index(fields=['company_name']),
            models.Index(fields=['created_at']),
        ]


class UserBookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this discount")
    notification_enabled = models.BooleanField(
        default=True,
        help_text="Receive notifications about this discount"
    )

    def __str__(self):
        return f"{self.user.username} - {self.discount.title}"

    class Meta:
        unique_together = ('user', 'discount')
        ordering = ['-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    university = models.CharField(max_length=100, blank=True)
    student_email = models.EmailField(blank=True)
    is_email_verified = models.BooleanField(default=False)
    notification_preferences = models.JSONField(
        default=dict,
        help_text="User's notification preferences"
    )
    interests = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class DiscountClick(models.Model):
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name='clicks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['clicked_at']),
            models.Index(fields=['discount', 'clicked_at']),
        ]
