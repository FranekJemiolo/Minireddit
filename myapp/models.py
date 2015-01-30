import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

# The models for minireddit site. Change -> Now one user has one newsfeed
# so that everyone can customize theirs, and the user is from django.conf.

class Newsfeed(models.Model):
    newsfeed_id = models.CharField(max_length=50, unique=True, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    def __str__(self):
        return str(self.newsfeed_id)
    

class Category(models.Model):
    name = models.CharField(max_length=50, default="Insert category name", unique=True, primary_key=True)
    newsfeed = models.ManyToManyField(Newsfeed)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.name

class Article(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    article_url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    def __str__name(self):
        return self.name
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class ArticleComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    article = models.ForeignKey(Article)
    pub_date = models.DateTimeField('date published')
    comment_text = models.CharField(max_length=255)

class ArticleVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    article = models.ForeignKey(Article)
    pub_date = models.DateTimeField('date published')
    value = models.IntegerField(default=0)
    class Meta:
        unique_together = (("user", "article"),)
        
 
