from django.utils.html import format_html
from django.contrib import admin
from .models import *


@admin.register(Category)
class Category(admin.ModelAdmin):
    search_fields = ('name',)
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    

class ContextInline(admin.StackedInline):
    model = Contex
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'image_source', 'read_time', 'author', 'published', 'views', 'comments',
                    'created_at',)
    search_fields = ('title', 'intro')
    list_filter = ('author', 'published', 'category', 'tags')
    date_hierarchy = 'created_at'
    inlines = (ContextInline,)

    def image_source(self, obj):
        if obj.image:
            return format_html('<img src="{}" width = "160" height="90" />', obj.image.url)
        return '-'
    image_source.short_description = 'Image preview'