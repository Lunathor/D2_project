from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


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
    
    def __str__(self):
        return self.Author_to_user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text=_('category name'))
    
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text=_('Author of the Post'))
    
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory', help_text=_('Category name'))
    title = models.CharField(max_length=128, help_text=_('Title of post'))
    text = models.TextField(verbose_name=pgettext_lazy('help text for Post model', 'This is the help text'))
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
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


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


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        
    )
