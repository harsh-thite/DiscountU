# models.py
from django.db import models
class Discount(models.Model):
    name = models.CharField(max_length=100, default="Unnamed Discount")
    description = models.TextField(null=True, blank=True)  # Allowing null and blank here
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valid_until = models.DateField(null=True, blank=True)  # Optional expiration date

    def __str__(self):
        return self.name
