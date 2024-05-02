from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    Author_to_user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    
    def update_rating(self):
        postRate = self.post_set.aggregate(postRating=Sum('rating'))
        pRate = 0
        pRate += postRate.get('postRating')
        
        commentRate = self.Author_to_user.comment_set.aggregate(commentRating=Sum('rating'))
        cRate = 0
        cRate += commentRate.get('commentRating')
        
        self.ratingAuthor = pRate * 3 + cRate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def preview(self):
        return self.text[0:123] + '...'
    
    def __str__(self):
        return f'{self.title.title()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
