from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from myapp import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^top/$', views.top, name='top'),
    url(r'^(?P<page_number>\d+)/$', views.index_more, name='index_more'),
    url(r'^top/(?P<page_number>\d+)/$', views.top_more, name='top_more'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^advanced_search/$', views.advanced_search, name='advanced_search'),
    url(r'^\?search_name=(?P<user_name>\.+)', views.user_search, name='user_search'),
    url(r'^\?search_category=(?P<searched_category>\w+)&search_name_c=(?P<searched_name>.*)', views.categories_search, name='search_bar'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^\?category_name=(?P<category_name>.+)/$', views.categories_search, name='categories_search'),
    url(r'^mycategories/$', views.mycategories, name='mycategories'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'accounts/login/$', login, {'template_name': r'myapp/base_login.html'}, name='login'),
    url(r'^category=/(?P<category_name>.+)/article/(?P<article_id>\d+)/(?P<article_value>-?\d+)/$', views.article_vote, name='article_vote'),
    url(r'^category=/(?P<category_name>.+)/article/(?P<article_id>\d+)/$', views.article, name='article'),
    url(r'^category/(?P<category_name>.+)/$', views.category, name='category'),
    url(r'^category_create/$', views.category_create, name='category_creation'),
    url(r'^category_add/$', views.category_addition, name='category_addition'),
    url(r'^article_create/$', views.article_create, name='article_creation'),
)
