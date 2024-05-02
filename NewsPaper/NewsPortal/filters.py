from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='PostCategory__category',
        queryset=Category.objects.all(),
    
    )
    
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'postCategory__categoryThrough': ['exact'],
        }
