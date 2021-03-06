from django.contrib import admin
from django.conf import settings
from myapp.models import Newsfeed, Category, Article, ArticleComment, ArticleVote

# Register your models here.

class ArticleCommentInline(admin.TabularInline):
    model = ArticleComment

class ArticleVoteInline(admin.TabularInline):
    model = ArticleVote

class ArticleInline(admin.TabularInline):
    model = Article
    inlines = [ArticleCommentInline, ArticleVoteInline]

class NewsfeedInline(admin.TabularInline):
    model = Category.newsfeed.through


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'user']
    inlines = [ArticleInline, NewsfeedInline]

class NewsfeedAdmin(admin.ModelAdmin):
    fields = ['newsfeed_id', 'user']

    
    
    
class ArticleAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'article_url', 'category', 'pub_date', 'votes', 'user']
    inlines = [ArticleCommentInline, ArticleVoteInline]
    list_display = ('id', 'name', 'article_url', 'category', 'pub_date', 'user', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['name']
    
    
admin.site.register(Newsfeed, NewsfeedAdmin)
   
admin.site.register(Category, CategoryAdmin)

admin.site.register(Article, ArticleAdmin)
