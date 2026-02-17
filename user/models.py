from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Extended User model with profile fields for profile management"""
    name = models.CharField(max_length=255, blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username


class CreditCard(models.Model):
    """Credit Card model for storing user credit cards"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards')
    card_number = models.CharField(
        max_length=19,
        validators=[RegexValidator(r'^\d{13,19}$', 'Enter a valid card number')]
    )
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(
        max_length=4,
        validators=[RegexValidator(r'^\d{3,4}$', 'Enter a valid CVV')]
    )
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cardholder_name} - {self.card_number[-4:]}"
