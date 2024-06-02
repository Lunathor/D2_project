from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, PostDetail, NewsSearchList, NewsCreate, ArticleCreate, PostUpdate, PostDelete, subscriptions
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60)(NewsList.as_view()), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='news_detail'),
   path('search/', NewsSearchList.as_view(), name='news_search'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('article/create', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]
