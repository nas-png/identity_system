import hashlib
import random
from django.db import models
from datetime import date

class User(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Changed from 'phone'
    date_of_birth = models.DateField()
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    unique_hash = models.CharField(max_length=64, unique=True, blank=True)
    user_number = models.IntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add properties for template compatibility
    @property
    def unique_id(self):
        """Return user_number as string for templates"""
        return str(self.user_number) if self.user_number else ""
    
    @property
    def internal_hash(self):
        """Alias for unique_hash"""
        return self.unique_hash
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def save(self, *args, **kwargs):
        # Generate hash
        fullname = self.first_name + self.last_name
        hash_input = fullname + str(self.date_of_birth) + self.gender
        self.unique_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        # Generate unique 6-digit number
        if not self.user_number:
            while True:
                num = random.randint(100000, 999999)
                if not User.objects.filter(user_number=num).exists():
                    self.user_number = num
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_number})"