from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# # User Signup
# class Signup(models.Model):
   
#     Username = models.CharField(max_length=50, unique=True, verbose_name="Username")
#     Email = models.EmailField(unique=True, verbose_name="Email Address")
#     Password = models.CharField(max_length=128, verbose_name="Password")  # Use Django's password hashing for security

#     def __str__(self):
#         return self.Username
    
# User Profile
class Profile(models.Model):
    USER_TYPES = [
        ('Producer', 'Producer'),
        ('Recycler', 'Recycler'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    organization_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.organization_name} ({self.user_type})"

# Waste Listing
class WasteListing(models.Model):
    WASTE_TYPES = [
        ('Plastic', 'Plastic'),
        ('Organic', 'Organic'),
        ('Cardboard', 'Cardboard'),
        ('E-Waste', 'E-Waste'),
    ]
    producer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='waste_producer')
    waste_type = models.CharField(max_length=50, choices=WASTE_TYPES)
    description = models.TextField()
    quantity = models.FloatField(help_text="Quantity in kilograms or units")
    location = models.CharField(max_length=200)
    availability_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waste_type} - {self.quantity} kg (by {self.producer})"
    def clean(self):
        # Ensure that only Producers can create Waste Listings
        if self.producer.user_type != 'Producer':
            raise ValidationError("Only Producers can create Waste Listings.")

# Transaction
class Transaction(models.Model):
    waste_listing = models.ForeignKey(WasteListing, on_delete=models.CASCADE)
    recycler = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='waste_recycler')
    transaction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.waste_listing} -> {self.recycler}"
