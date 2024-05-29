from django.db import models

# Create your models here.
class UserModel(models.Model):
    name=models.CharField(max_length=100)
    profile_image=models.ImageField(upload_to='profile_image')
    def __str__(self):
        return self.name