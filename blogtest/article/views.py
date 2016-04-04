from django.shortcuts import render,redirect
from markdown import markdown
from django.http import HttpResponse
from datetime import datetime
from models import Article
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
import csv
# Create your views here.

def home(request):
    post_list = Article.objects.all()

    paginator = Paginator(post_list,2)

    try:
        page = request.GET.get('page')
        if page <1:
            page = 1
    except ValueError:
        page = 1

    try :
        post_list = paginator.page(page)
    except (PageNotAnInteger,EmptyPage,InvalidPage):
        post_list = paginator.page(1)
    return render(request,'home.html',{'post_list' : post_list})


def detail(request, id):
    try:
        post = Article.objects.get(id = str(id))
    except Article.DoesNotExist:
        raise Http404

    return render(request,'post.html',{'post':post})

def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request,'archives.html',{'post_list':post_list,'error':False})

def about_me(request):
    return render(request,'aboutme.html')

def search_tag(request, tag) :
    try:
        post_list = Article.objects.filter(category__iexact = tag) #contains
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list})

def blog_search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        post_list = Article.objects.filter(title__icontains = q)
        if len(post_list) == 0:

            return render(request,'archives.html',{'post_list':post_list,'error':True})
        else:
            return render(request,'archives.html',{'error':False,'post_list':post_list})

    return redirect('/')


class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    # def item_pubdate(self, item):
    #     return item.add_date

    def item_description(self, item):
        return item.content

