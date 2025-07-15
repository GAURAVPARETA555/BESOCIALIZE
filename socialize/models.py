from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=300)
    photo = models.ImageField(upload_to='photos/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    like= models.ManyToManyField(User,related_name='liked_tweets',blank=True)
    share_count= models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    
class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    tweet=models.ForeignKey(Tweet,on_delete=models.CASCADE,related_name='comments')
    text=models.CharField(50)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username}-{self.text[:20]}'