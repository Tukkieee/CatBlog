from django.db import models
from accounts.models import UserAccount
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
    

class Blog(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='blogs',)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created= models.DateTimeField(auto_now_add=True, editable=False)
    date_published = models.DateTimeField(auto_now=True, editable=False)
    publish = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='blog_img/',default="/blog_img/default.png" )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
    
    def get_description_snippet(self):  
        return f'{self.description[:150]}...'
    def publish_post(self):
        self.publish = True
        self.date_published= timezone.now()
     
    def unpublish_post(self):
        self.publish = False
        self.date_published = None
        
    def count_comment(self):
        return self.comments.count()
    
    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    profile_Image = models.ImageField(upload_to='comment_img/', default="comment_img/default.png")
    
    def save(self, *args, **kwargs):
        if self.user is not None:
            if self.user.is_authenticated:
                self.profile_Image = self.user.profile_image
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.message}'



class Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    like = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.blog.title} - Likes: {self.like}'