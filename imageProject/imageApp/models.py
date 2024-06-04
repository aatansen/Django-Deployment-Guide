from django.db import models
from django_cleanup import cleanup

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.name}_{filename}"

@cleanup.select
class UserModel(models.Model):
    name=models.CharField(max_length=100)
    profile_image=models.ImageField(upload_to=user_directory_path)
    def __str__(self):
        return self.name