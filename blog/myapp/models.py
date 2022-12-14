from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    """Модель статей"""

    header = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.title

    def tags(self):
        return self.tag.split(', ')

    @classmethod
    def get_most_common_tags(cls):
        tags = []
        for post in cls.objects.all()[:7]:
            for tag in post.tags():
                if tag not in tags:
                    tags.append(tag)
        return tags


class Comment(models.Model):
    """Модель комментариев"""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_name'
    )
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text
