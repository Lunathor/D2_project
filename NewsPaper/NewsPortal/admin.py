from django.contrib import admin
from .models import Post, PostCategory, Category
from modeltranslation.admin import TranslationAdmin


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullify_rating.short_description = 'Обнулить рейтинг'


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostTransAdmin(TranslationAdmin):
    model = Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'dateCreation', 'rating']
    list_filter = ['title', 'dateCreation', 'rating']
    search_fields = ('title', 'postCategory__name')
    actions = [nullify_rating]


admin.site.register(Post, PostAdmin)
admin.site.register(PostTransAdmin)
admin.site.register(PostCategory)
admin.site.register(Category, CategoryAdmin)
