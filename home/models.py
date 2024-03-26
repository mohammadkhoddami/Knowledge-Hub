from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name = 'posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.slug
    

    def get_absolute_url(self):
        return reverse('home:post', args=(self.id , self.slug))
    

    def like_count(self):
        return self.pvote.count()
    
    def user_can_like(self, user):
        user_like = user.uvote.filter(post=self)
        if user_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'ucomments')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'pcomments')
    reply = models.ForeignKey('self', on_delete = models.CASCADE, related_name = 'rcomments', blank = True, null = True)
    is_reply = models.BooleanField(default = False)
    body = models.TextField(max_length = 400)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f'{self.user} - {self.body[:30]}'



class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'pvote')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'uvote')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
    


