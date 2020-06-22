from django.contrib import admin

from .models import Review, Title, Comment, Category, Genre,Client

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--'

class ReviewAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'pub_date', 'author', 'title', 'score') 
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text","title",) 
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",) 

class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('name',)
    #empty_value_display = '--'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'review', 'pub_date')
    search_fields = ('review',)
    list_filter = ('review',)
    #empty_value_display = '--'

    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Client)
