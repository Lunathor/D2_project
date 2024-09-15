from .models import *
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)


@register(Post)
class PostTranslatorOption(TranslationOptions):
    fields = ('category_type', 'postCategory',)
    
    
