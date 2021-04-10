from django.shortcuts import render
from datetime import datetime
from .forms import DomainForm
import vk
from jetbrains_vk.models import Choice

def index(request):
    if request.method == "POST":
        domain = request.POST.get ("domain")

        session = vk.Session (access_token='723789a4723789a4723789a4037240c0a577237723789a4125960cfa0d6d1f20e095818')
        api = vk.API (session)

        # Получаю массив id_posts с ид всех постов сообщества/человека
        wall=api.wall.get(owner_id=int('-{}'.format(domain)),count=1,v=5.71)
        count_wall=int(wall['count'])
        id_posts=[]
        offset_wall=0
        while count_wall > len(id_posts):
            wall = api.wall.get (owner_id=int('-{}'.format(domain)), offset=offset_wall ,count=100, v=5.71)
            offset_wall += 100
            for wall in wall['items']:
                id_posts.append(wall['id'])

        # Получаю все комментарии поста
        for id_post in id_posts:
            all_comments_post = []
            offset_comments = 0
            comments = api.wall.getComments(owner_id=int('-{}'.format(domain)), post_id=id_post, count=1, v=5.71)
            count_comments = int (comments ['count'])
            while count_comments>len(all_comments_post):
                comments = api.wall.getComments (owner_id=int ('-{}'.format (domain)), offset=offset_comments, post_id=id_post, count=100, v=5.71)
                offset_comments += 100
                for comment in comments['items']:
                    all_comments_post.append([comment['from_id'], comment['likes']['count'], comment['date']])

        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})
    else:
        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})