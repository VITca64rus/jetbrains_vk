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
        wall=api.wall.get(domain=domain,count=1,v=5.71)
        count_wall=int(wall['count'])
        id_posts=[]
        offset_wall=0
        while count_wall > len(id_posts):
            wall = api.wall.get (domain=domain, offset=offset_wall ,count=100, v=5.71)
            offset_wall += 100
            for wall in wall['items']:
                id_posts.append(wall['id'])


        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})
    else:
        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})