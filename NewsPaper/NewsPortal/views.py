from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Subscriber, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import info_after_new_post



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
    
    
class NewsSearchList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'search.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
    
class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPaper.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        # info_after_new_post.delay(form.instance.pk)
        return super().form_valid(form)
    
    
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        # info_after_new_post.delay(form.instance.pk)
        return super().form_valid(form)
    
    
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    
    
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    
    
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        
        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()
            
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions}
    )
