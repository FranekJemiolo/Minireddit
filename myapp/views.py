import datetime

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings
from myapp.models import Newsfeed, Category, Article, ArticleComment, ArticleVote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp.forms import UserForm, CategoryForm, ArticleForm, CommentForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def signin(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
            newsfeed = Newsfeed(newsfeed_id=user.username, user=user)
            newsfeed.save()
        else:
            print user_form.errors
    else:
        user_form = UserForm()
        
    return render_to_response(
        'myapp/base_signin.html',
        {'user_form': user_form, 'registered': registered},
        context
    )

def auth_view(request):
    user_form = UserForm(data=request.POST)
    user = authenticate(username=user_form.username, password=user_form.password)
    if user is not None and user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/myapp/')
    else:
        # Return an 'invalid login' error message
        #return invalid(self)
        print user_form.errors
    return render_to_response(
        'myapp/base_login.html',
        {'user_form': user_form},
        context
    )
        
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'myapp/base_logout.html')

@login_required  
def index(request):
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    
    latest_articles_list = Article.objects.order_by('-pub_date')[:20]
    is_all = Article.objects.count() <= 20
    page_num = 2
    context = {
        'latest_articles_list': latest_articles_list,
        'page_num': page_num,
        'is_all': is_all,
    }
    return render(request, 'myapp/base_index.html', context)

@login_required  
def index_more(request, page_number):
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    page_num = int(page_number)
    count = 20*page_num
    is_all = Article.objects.count() <= count
    page_num = page_num+1
    latest_articles_list = Article.objects.order_by('-pub_date')[:count]
    context = {
        'latest_articles_list': latest_articles_list,
        'page_num': page_num,
        'is_all': is_all,
    }
    return render(request, 'myapp/base_index.html', context)

@login_required  
def top(request):
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    top_articles_list = Article.objects.order_by('-votes')[:20]
    is_all = Article.objects.count() <= 20
    page_num = 2
    context = {
        'top_articles_list': top_articles_list,
        'page_num': page_num,
        'is_all': is_all,
    }
    return render(request, 'myapp/base_top.html', context)


@login_required  
def top_more(request, page_number):
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    page_num = int(page_number)
    count = 20*page_num
    is_all = Article.objects.count() <= count
    page_num = page_num+1
    top_articles_list = Article.objects.order_by('-votes')[:count]
    context = {
        'top_articles_list': top_articles_list,
        'page_num': page_num,
        'is_all': is_all,
    }
    return render(request, 'myapp/base_top.html', context)

@login_required   
def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    article_list = Article.objects.filter(category=category_name)
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    return render(request, 'myapp/base_category.html', 
        {'category': category, 'article_list': article_list}
    )

@login_required    
def article(request, category_name, article_id):
    category = get_object_or_404(Category, name=category_name)
    article = get_object_or_404(Article, id=article_id, category=category)
    comment_list = ArticleComment.objects.filter(article=article).order_by('-pub_date')
    posted = False
    context = RequestContext(request)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        user = request.user
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            comment = ArticleComment(user=user, article=article, comment_text=comment_text, pub_date=timezone.now())
            comment.save()
            article.comments = article.comments+1
            article.save()
            posted = True
        else:   
            print comment_form.errors
    else:
        comment_form = CommentForm()
        #Search bar methods
        if request.method == 'GET' and 'search_category_button' in request.GET:
            search_category = request.GET.get('search_category')
            category_name = request.GET.get('search_name_c')
            if (category_name is not None) and (search_category is not None):
                return search_bar(request, search_category, category_name)
        if request.method == 'GET' and 'search_user_button' in request.GET:
            user_name = request.GET.get('search_name')
            if user_name is not None:
                return user_search(request, user_name)
    return render_to_response(
        'myapp/base_article.html',
        {'posted': posted, 'article': article, 'comment_list': comment_list},
        context
    )
    
    
@login_required
def category_create(request):
    alreadycreated = False
    created = False
    context = RequestContext(request)
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)
        user = request.user
        
        if category_form.is_valid():
            category_name = category_form.cleaned_data['name']
            category_ex = Category.objects.filter(name=category_name)
            if category_ex.exists():
                alreadycreated = True
            else:
                category = Category(name=category_name, user=user, pub_date=timezone.now())
                category.save()
                created = True
            
        else:
            create = False
            alreadycreated = True
    else:
        category_form = CategoryForm()
        #Search bar methods
        if request.method == 'GET' and 'search_category_button' in request.GET:
            search_category = request.GET.get('search_category')
            category_name = request.GET.get('search_name_c')
            if (category_name is not None) and (search_category is not None):
                return search_bar(request, search_category, category_name)
        if request.method == 'GET' and 'search_user_button' in request.GET:
            user_name = request.GET.get('search_name')
            if user_name is not None:
                return user_search(request, user_name)
    return render_to_response(
        'myapp/base_category_create.html',
        {'alreadycreated': alreadycreated, 'created': created},
        context
    )
    
@login_required
def article_create(request):
    alreadycreated = False
    created = False
    category_list = Category.objects.order_by('name')
    context = RequestContext(request)
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST)
        user = request.user
        if article_form.is_valid():
            article_name = article_form.cleaned_data['name']
            article_url = article_form.cleaned_data['article_url']
            category_name = article_form.cleaned_data['category_name']
            category = get_object_or_404(Category, name=category_name)
            time = timezone.now()
            article = Article(name=article_name, article_url=article_url, user=user, category=category, pub_date=time)
            article.save()
            created = True
            
        else:
            alreadycreated = True
    else:
        article_form = ArticleForm()
        #Search bar methods
        if request.method == 'GET' and 'search_category_button' in request.GET:
            search_category = request.GET.get('search_category')
            category_name = request.GET.get('search_name_c')
            if (category_name is not None) and (search_category is not None):
                return search_bar(request, search_category, category_name)
        if request.method == 'GET' and 'search_user_button' in request.GET:
            user_name = request.GET.get('search_name')
            if user_name is not None:
                return user_search(request, user_name)
    return render_to_response(
        'myapp/base_article_create.html',
        {'alreadycreated': alreadycreated, 'created': created, 'category_list': category_list},
        context
    )
    

def about(request):
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)    
    return render(request, 'myapp/base_about.html')
    

def contact(request):
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)    
    return render(request, 'myapp/base_contact.html')    


@login_required   
def categories(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('name')
    mycategories = False
    #Categories search
    if request.method == 'GET' and 'category_form_button' in request.GET:
        category_name = request.GET.get('category_name')
        if category_name is not None:
            return categories_search(request, category_name)
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    return render_to_response('myapp/base_categories.html',{'mycategories': mycategories, 'category_list': category_list} ,context)  
    
@login_required    
def mycategories(request):
    context = RequestContext(request)
    user = request.user
    newsfeed = Newsfeed.objects.get_or_create(newsfeed_id=user.username, user = user)
    category_list = Category.objects.filter(newsfeed=newsfeed)
    mycategories = True
    if request.method == 'GET' and 'category_form_button' in request.GET:
        category_name = request.GET.get('category_name')
        if category_name is not None:
            return categories_search(request, category_name, mycategories)
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    return render_to_response('myapp/base_categories.html',{'mycategories': mycategories, 'category_list': category_list} ,context)     

@login_required    
def category_addition(request): 
    context = RequestContext(request)
    user = request.user
    added = False
    newsfeed, created = Newsfeed.objects.get_or_create(newsfeed_id=user.username, user=user)
    available_category_list = Category.objects.all().exclude(newsfeed=newsfeed)
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)
        if category_form.is_valid():
            category_name = category_form.cleaned_data['name']
            category = Category.objects.get(name=category_name)
            category.newsfeed.add(newsfeed)
            category.save()
            added = True
        else:
            return HttpResponse("WRONG FORM")
    else:
        category_form = CategoryForm()
        #Search bar methods
        if request.method == 'GET' and 'search_category_button' in request.GET:
            search_category = request.GET.get('search_category')
            category_name = request.GET.get('search_name_c')
            if (category_name is not None) and (search_category is not None):
                return search_bar(request, search_category, category_name)
        if request.method == 'GET' and 'search_user_button' in request.GET:
            user_name = request.GET.get('search_name')
            if user_name is not None:
                return user_search(request, user_name)
    return render_to_response(
        'myapp/base_category_add.html',
        {'added': added, 'created': created, 'available_category_list': available_category_list},
        context
    )
  
  
@login_required   
def categories_search(request, category_name, mycategories=False):
    searched_result = True
    if mycategories:
        user = request.user
        newsfeed = Newsfeed.objects.get_or_create(newsfeed_id=user.username, user = user)
        category_list = Category.objects.filter(newsfeed=newsfeed, name__startswith=category_name)
    else:
        category_list = Category.objects.filter(name__startswith=category_name)
        
    context = {'mycategories': mycategories, 'category_list': category_list, 'searched_result': searched_result}
    #Search bar methods
    #if request.method == 'GET' and 'search_category_button' in request.GET:
    #    search_category = request.GET.get('search_category')
    #    category_name = request.GET.get('search_name_c')
    #    if (category_name is not None) and (search_category is not None):
    #        return search_bar(request, search_category, category_name)
    #if request.method == 'GET' and 'search_user_button' in request.GET:
    #    user_name = request.GET.get('search_name')
    #    if user_name is not None:
    #        return user_search(request, user_name)
    return render(
        request,
        'myapp/base_categories.html',
        context     
    )      

@login_required
def user_search(request, user_name):
    try:
        searched_user = User.objects.get(username=user_name)
    except ObjectDoesNotExist:
        searched_user = None
    article_list = Article.objects.filter(user=searched_user)
    context = {'article_list': article_list, 'searched_user': searched_user}
    return render(
        request,
        'myapp/base_user_search.html',
        context
    )

@login_required
def article_search(request, search_name):
    article_list = Article.objects.filter(name__startswith=search_name)
    context = {'article_list': article_list}
    return render(
        request,
        'myapp/base_article_search.html',
        context
    )
  
@login_required
def search_bar(request, search_category, search_name):
    if search_category == "categories":
        return categories_search(request, search_name)
    elif search_category == "mycategories":
        mycategories = True
        return categories_search(request, search_name, mycategories)
    elif search_category == "articles":
        return article_search(request, search_name)
    else:    
        return render(request, 'myapp/base_search.html')


@login_required
def article_vote(request, category_name, article_id, article_value):
    article = Article.objects.get(id=article_id)
    user = request.user
    voted = True
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        user = request.user
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            comment = ArticleComment(user=user, article=article, comment_text=comment_text, pub_date=timezone.now())
            comment.save()
            article.comments = article.comments+1
            article.save()
            posted = True
        else:   
            print comment_form.errors
    else:
        comment_form = CommentForm()
        if request.method == 'GET' and 'search_category_button' in request.GET:
            search_category = request.GET.get('search_category')
            category_name = request.GET.get('search_name_c')
            if (category_name is not None) and (search_category is not None):
                return search_bar(request, search_category, category_name)
        if request.method == 'GET' and 'search_user_button' in request.GET:
            user_name = request.GET.get('search_name')
            if user_name is not None:
                return user_search(request, user_name)
    try:
        article_vote = ArticleVote.objects.get(user=user, article=article)
        already_voted = True
        comment_list = ArticleComment.objects.filter(article=article).order_by('-pub_date')
        posted = False
        context = {'already_voted': already_voted, 'posted': posted, 'comment_list': comment_list, 'article': article, 'voted': voted}
        return render(
            request,
            'myapp/base_article.html',
            context
        )
    except:
        article_vote = ArticleVote(user=user, article=article, pub_date=timezone.now(), value=int(article_value))
        article_vote.save()
        article.votes = article.votes + int(article_value)
        article.save()
        already_voted = False
        comment_list = ArticleComment.objects.filter(article=article).order_by('-pub_date')
        posted = False
        context = {'already_voted': already_voted, 'posted': posted, 'comment_list': comment_list, 'article': article, 'voted': voted}
        return render(
            request,
            'myapp/base_article.html',
            context
        )
        
    return article(request, category_name, article_id)

@login_required
def advanced_search_results(request, search_time, search_order, search_by, search_category, search_name_advanced):
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    article_list = Article.objects.all()
    now = timezone.now()
    if search_time == "today":
        article_list = article_list.filter(pub_date__range=[now-datetime.timedelta(days=1), now])
    elif search_time == "7_days":
        article_list = article_list.filter(pub_date__range=[now-datetime.timedelta(days=7), now])
    elif search_time == "30_days":
        article_list = article_list.filter(pub_date__range=[now-datetime.timedelta(days=30), now])
    #elif search_time == "All time": we already gathered everythinh
    
    if search_order == "rising":
        if search_by == "votes":
            article_list = article_list.order_by('votes')
        elif search_by == "pub_date":
            article_list = article_list.order_by('pub_date')
        elif search_by == "name":
            article_list = article_list.order_by('name')
        
    elif search_order == "lowering":
        if search_by == "votes":
            article_list = article_list.order_by('-votes')
        elif search_by == "pub_date":
            article_list = article_list.order_by('-pub_date')
        elif search_by == "name":
            article_list = article_list.order_by('-name')
    
    #if search_category == "Categories": we dont have to do that because it means all categories
        
    if search_category == "mycategories":
        user = request.user
        newsfeed = Newsfeed.objects.get(user=user)
        category_list = Category.objects.filter(newsfeed=newsfeed)
        article_list = article_list.filter(category=category_list)
        
    article_list = article_list.filter(name__startswith=search_name_advanced)
    context = {'article_list': article_list}
    return render (request, 'myapp/base_advanced_search_results.html', context)
        
      

    
@login_required    
def advanced_search(request):
    context = RequestContext(request)
    #Search bar methods
    if request.method == 'GET' and 'search_category_button' in request.GET:
        search_category = request.GET.get('search_category')
        category_name = request.GET.get('search_name_c')
        if (category_name is not None) and (search_category is not None):
            return search_bar(request, search_category, category_name)
    if request.method == 'GET' and 'search_user_button' in request.GET:
        user_name = request.GET.get('search_name')
        if user_name is not None:
            return user_search(request, user_name)
    if request.method == 'GET' and 'advanced_search_button' in request.GET:
        search_time = request.GET.get('search_time')
        search_order = request.GET.get('search_order')
        search_by = request.GET.get('search_by')
        search_category = request.GET.get('search_category')
        search_name_advanced = request.GET.get('search_name_advanced')
        if (search_time is not None) and (search_order is not None) and (search_by is not None) and (search_category is not None) and (search_name_advanced is not None):
            return advanced_search_results(
                request, search_time, 
                search_order, search_by, 
                search_category, search_name_advanced
            ) 
        
    return render_to_response('myapp/base_advanced_search.html', context)
