from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    
    
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'news'
