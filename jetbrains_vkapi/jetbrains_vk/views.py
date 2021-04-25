from django.shortcuts import render
from datetime import datetime
from .forms import DomainForm
import vk
from jetbrains_vk.models import Choice
from django.db.models import Count, Sum
import time
from django.http import HttpResponse, JsonResponse

def index(request):

    if request.method == "POST":
        Choice.objects.all ().delete ()
        domain = request.POST.get ("domain")
        data1 = datetime.strptime(request.POST.get ("data1"), '%m/%d/%Y %H:%M %p')
        data2 = datetime.strptime(request.POST.get ("data2"), '%m/%d/%Y %H:%M %p')
        data1_stamp = int(data1.timestamp())
        data2_stamp = int(data2.timestamp())
        what = request.POST.get ("what")
        print(domain,data1,data2,what)
        domainform = DomainForm ()


        session = vk.Session (access_token='723789a4723789a4723789a4037240c0a577237723789a4125960cfa0d6d1f20e095818')
        api = vk.API (session)

        # Получаю массив id_posts с ид всех постов сообщества/человека
        try:
            wall=api.wall.get(owner_id=int('-{}'.format(domain)),count=1,v=5.71)
        except (vk.exceptions.VkAPIError, ValueError):
            try:
                wall=api.wall.get(owner_id=int('{}'.format(domain)),count=1,v=5.71)
            except (vk.exceptions.VkAPIError, ValueError):
                domainform = DomainForm ()
                return render (request, "index.html", {"form": domainform, 'fail': 'Некорректный id сообщества'})

        count_wall=int(wall['count'])
        id_posts=[]
        offset_wall=0
        data_stat = True
        while (count_wall > len(id_posts)):
            try:
                wall = api.wall.get (owner_id=int('-{}'.format(domain)), offset=offset_wall ,count=100, v=5.71)
            except (vk.exceptions.VkAPIError, ValueError):

                try:
                    wall = api.wall.get (owner_id=int ('{}'.format (domain)), offset=offset_wall, count=100, v=5.71)
                except (vk.exceptions.VkAPIError, ValueError):
                    domainform = DomainForm ()
                    return render (request, "index.html", {"form": domainform, 'fail': 'Некорректный id сообщества'})
            offset_wall += 100
            for wall in wall['items']:
                if int(what)==2:
                    print('what==2')
                    print(int(wall['date']),'>',data1_stamp,'and',int(wall['date']),'<',data2_stamp)
                    if int(wall['date'])>data1_stamp and int(wall['date'])<data2_stamp:
                        id_posts.append (wall ['id'])
                        print(id_posts)
                    else:
                        count_wall -= 1
                else:
                    id_posts.append (wall ['id'])

        #Получаю все комментарии по каждому посту
        for id_post in id_posts:
            print('id_post', id_post)
            offset_comments = 0
            all_comments = []
            count_comments = 1

            while count_comments > len(all_comments):
                try:
                    comments = api.wall.getComments(owner_id=int('-{}'.format(domain)), post_id=id_post, offset=offset_comments, need_likes=1,
                                                    count=100, v=5.91)
                except (vk.exceptions.VkAPIError, ValueError):
                    pass
                try:
                    comments = api.wall.getComments(owner_id=int('{}'.format(domain)), post_id=id_post, offset=offset_comments, need_likes=1,
                                                    count=100, v=5.91)
                except (vk.exceptions.VkAPIError, ValueError):
                    pass

                offset_comments += 100
                count_comments = comments['count']
                for comment in comments['items']:

                    print(comment)
                    try:
                        all_comments.append([comment['from_id'], comment['likes']['count'], comment['date']])
                    except:
                        all_comments.append (['-', 0, comment ['date']])
                    #print('comments',[comment['from_id'], comment['likes']['count'], comment['date']])
                    id_comment=comment['id']
                    count_threads = 1
                    offset_threads = 0
                    len_before_threads=len(all_comments)
                    while count_threads > len(all_comments)-len_before_threads:
                        print(count_threads+len(all_comments),len(all_comments))
                        try:
                            threads = api.wall.getComments(owner_id=int('-{}'.format(domain)), post_id=id_post, offset=offset_threads, need_likes=1,
                                                        count=10, comment_id=id_comment, v=5.91)
                        except (vk.exceptions.VkAPIError, ValueError):
                            pass
                        try:
                            threads = api.wall.getComments(owner_id=int('{}'.format(domain)), post_id=id_post, offset=offset_threads, need_likes=1,
                                                        count=10, comment_id=id_comment, v=5.91)
                        except (vk.exceptions.VkAPIError, ValueError):
                            pass
                        offset_threads += 10
                        count_threads = threads['count']
                        for thread in threads['items']:
                            all_comments.append ([thread ['from_id'], thread ['likes'] ['count'], thread ['date']])
                            print('threads',[thread ['from_id'], thread ['likes'] ['count'], thread ['date']])

            #Загружаю все комментарии поста в БД
            print('НАЧАЛ ЗАГРУЗКУ В БД')
            print(all_comments)
            #comments_bd = Choice()
            for comment_ in all_comments:
                if int(what) == 3:
                    if int(comment_[2])>data1_stamp and int(comment_[2])<data2_stamp:
                        comments_bd = Choice ()
                        comments_bd.id_user = comment_[0]
                        print(time.strftime("%Y/%m/%d", time.localtime(int(comment_[2]))))
                        comments_bd.date = time.strftime("%Y-%m-%d", time.localtime(int(comment_[2])))
                        comments_bd.likes_count = comment_[1]
                        comments_bd.save()
                else:
                    comments_bd = Choice ()
                    comments_bd.id_user = comment_ [0]
                    print (time.strftime ("%Y/%m/%d", time.localtime (int (comment_ [2]))))
                    comments_bd.date = time.strftime ("%Y-%m-%d", time.localtime (int (comment_ [2])))
                    comments_bd.likes_count = comment_ [1]
                    comments_bd.save ()

        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})
    else:
        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})


def graph(request):
    # Делаю запросы к БД строю графики

    # Вытаскиваю инфу из БД для графика - Пользователи с наибольшим количеством комментариев
    user_countcomment = Choice.objects.values ('id_user').annotate (total=Count ('id'))
    user = []
    count = []
    for user_count in user_countcomment:
        user.append ('id ' + str(user_count ['id_user']))
        count.append ((user_count ['total']))

    # Вытаскиваю инфу из БД для графика -  Пользователи с наибольшим количеством лайков
    user_countlikes = Choice.objects.values ('id_user').annotate (total=Sum ('likes_count'))
    user1 = []
    count1 = []
    for user_count in user_countlikes:
        user1.append ('id ' + str(user_count ['id_user']))
        count1.append ((user_count ['total']))

    # Вытаскиваю инфу из БД для графика -  Кол-во комментариев по дням
    day_countcomments = Choice.objects.values ('date').annotate (total=Count ('id'))
    day = []
    count_comm = []
    for day_count in day_countcomments:
        day.append (day_count ['date'])
        count_comm.append ((day_count ['total']))

    # Вытаскиваю инфу из БД для графика -  Кол-во уникальных комментаторов по дням
    day_countuser = Choice.objects.values ('date').annotate (total=Count ('id_user', distinct=True))
    day1 = []
    count_user1 = []
    for day_count in day_countuser:
        day1.append (day_count ['date'])
        count_user1.append (day_count ['total'])

    res={
        'first': [user, count],
        'second': [user1, count1],
        'third': [day, count_comm],
        'four': [day1, count_user1]
    }
    return JsonResponse(res, safe=False)