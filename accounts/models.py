from django.db import models
# from blogs.models import Blog
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserAccount(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_img/', default="profile_img/default.png")

    def count_published(self):
       return self.blogs.filter(publish=True).count()
    
    def count_unpublished(self):
       return self.blogs.filter(publish=False).count()
    
    def __str__(self):
        return f'{self.username}'
