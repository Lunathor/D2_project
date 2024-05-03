from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(field_name='postCategory',
                                 queryset=Category.objects.all(),
                                 empty_label='Все',
                                 )
    
    created_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )
    
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
