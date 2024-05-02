from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(field_name='postCategory',
                                 queryset=Category.objects.all(),
                                 empty_label='Все',
                                 )
    
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
