from django.db import models
from django_cleanup import cleanup
from django.contrib.auth.models import AbstractUser

# Create your models here.
def user_directory_path(instance, filename):
    return f"user_{instance.name}_added_by_{instance.created_by.username}_{filename}"

class CustomUserModel(AbstractUser):
    def __str__(self):
        return self.username

@cleanup.select
class UserModel(models.Model):
    created_by = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='user_models')
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=user_directory_path)
    def __str__(self):
        return f"{self.name} added by {self.created_by.username}"


