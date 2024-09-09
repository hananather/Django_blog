from django.db import models
from django.utils import timezone
from django.conf import settings

    
class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return (super().get_queryset().filter(status = Post.Status.PUBLISHED))


class Post(models.Model):
    
    objects = models.Manager() # default manager
    published = PublishedManager() # Our custom manager
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(  # Add this new field for status
        max_length=2,
        choices=Status.choices,  # Use .choices here
        default=Status.DRAFT
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts"
    )
    
    
    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"])
        ]
    
    def __str__(self):
        return self.title