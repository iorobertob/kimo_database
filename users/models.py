from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Administrator'),
        ('librarian', 'Librarian'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('guest', 'Guest'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='guest')
    institution = models.CharField(max_length=100, blank=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    federated_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def can_add_films(self):
        return self.user_type in ['admin', 'librarian']
    
    def can_access_api(self):
        return self.user_type in ['admin', 'librarian', 'student', 'faculty']
    
    def can_manage_users(self):
        return self.user_type == 'admin'