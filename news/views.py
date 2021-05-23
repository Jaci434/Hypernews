from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
import json
from django.conf import settings
from datetime import datetime
import random
import re

with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    posts = json.load(json_file)

class NewsView(View):
    def get(self, request, *args, **kwargs):
        search = str(request.GET.get('q'))
        search_posts = []
        for item in posts:
            if re.search(search, item['title']):
                search_posts.append(item)

        if search_posts != []:
            context = {'posts': search_posts}
        else:
            context = {'posts': posts}
        return render(request, "news/NewsMainPage.html", context)

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')

class ArticleView(View):
    def get(self, request, link):
        for item in posts:
            if item["link"] == link:
                artic = item
        return render(request, 'news/article.html', context=artic)

class CreateArticle(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/CreateArticle.html')

    def post(self, request, *args, **kwargs):
        article = {}
        title = request.POST.get('title')
        text = request.POST.get('text')
        article['title'] = title
        article['text'] = text
        article['created'] = str(datetime.now())
        new_link = random.randint(0, 100)
        check_link = [item['link'] for item in posts if item['link'] == new_link]
        if check_link == []:
            article['link'] = new_link

        posts.append(article)
        with open(settings.NEWS_JSON_PATH, 'w') as json_write:
            json.dump(posts, json_write)

        return redirect('/news/')

