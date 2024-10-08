from django.contrib import admin
from .models import Post, PostCategory, Category
from modeltranslation.admin import TranslationAdmin


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullify_rating.short_description = 'Обнулить рейтинг'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_filter = ['name', ]
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'dateCreation', 'rating']
    list_filter = ['title', 'dateCreation', 'rating']
    search_fields = ('title', 'postCategory__name')
    actions = [nullify_rating]


class TransCategoryAdmin(CategoryAdmin, TranslationAdmin):
    model = Category


class TransPostAdmin(PostAdmin,TranslationAdmin):
    model = Post


admin.site.register(Post, TransPostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category, TransCategoryAdmin)
