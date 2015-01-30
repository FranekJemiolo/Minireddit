from django.contrib.auth.models import User
from myapp import models
from django import forms
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class CategoryForm(forms.Form):
    name = forms.CharField(max_length=50)
    
class ArticleForm(forms.Form):
    article_url = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
    category_name = forms.CharField(max_length=50)
    
class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=255)
    

