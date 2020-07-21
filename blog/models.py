from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    liked = models.ManyToManyField(User, default=None, blank=True,related_name='liked')
    comments=models.ManyToManyField(User,default=None,blank=True,related_name='comments')
    draft=models.BooleanField(default=False,null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    @property
    def total_likes(self):
    	return self.liked.all().count()

# class Comments(models.Model):
#     comment = models.TextField();
#     author = models.ForeignKey(User,on_delete=models.CASCADE)
#     date_posted = models.DateTimeField(default=timezone.now)
#     post = models.ForeignKey(Post,on_delete=models.CASCADE)

LIKE_OR_UNLIKE = {

		('Like','Like'),
		('Unlike','Unlike'),
}

class Likes(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_OR_UNLIKE,default='Like',max_length=10)

    def __str__(self):
    	return str(self.post)

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author','post'],name='unique_comment')
        ]