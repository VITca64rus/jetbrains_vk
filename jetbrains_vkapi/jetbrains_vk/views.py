from django.shortcuts import render
from datetime import datetime
from .forms import DomainForm
import vk
from jetbrains_vk.models import Choice
from django.db.models import Count, Sum
import matplotlib.pyplot as plt
import time

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


        #Получаю все комментарии по каждому посту
        for id_post in id_posts:
            print('id_post', id_post)

            offset_comments = 0
            all_comments = []
            count_comments = 1
            while count_comments > len(all_comments):
                comments = api.wall.getComments(owner_id=int('-{}'.format(domain)), post_id=id_post, offset=offset_comments, need_likes=1,
                                                count=100, v=5.91)
                offset_comments += 100
                count_comments = comments['count']
                for comment in comments['items']:
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
                        threads = api.wall.getComments(owner_id=int('-{}'.format(domain)), post_id=id_post, offset=offset_threads, need_likes=1,
                                                        count=10, comment_id=id_comment, v=5.91)
                        offset_threads += 10
                        count_threads = threads['count']
                        for thread in threads['items']:
                            all_comments.append ([thread ['from_id'], thread ['likes'] ['count'], thread ['date']])
                            print('threads',[thread ['from_id'], thread ['likes'] ['count'], thread ['date']])


            #Загружаю все комментарии поста в БД
            print('НАЧАЛ ЗАГРУЗКУ В БД')
            comments_bd = Choice()
            for comment_ in all_comments:
                comments_bd.id_user = comment_[0]
                comments_bd.date = time.strftime("%D", time.localtime(int(comment_[2])))
                comments_bd.likes_count = comment_[1]
                comments_bd.save()

      #  print(time.strftime("%D", time.localtime(int('1284101485'))))

        #Делаю запросы к БД строю графики

        #Вытаскиваю инфу из БД для графика - Пользователи с наибольшим количеством комментариев
        user_countcomment = Choice.objects.values ('id_user').annotate(total=Count('id'))
        user=[]
        count=[]
        for user_count in user_countcomment:
            user.append(user_count['id_user'])
            count.append((user_count['total']))

        # Вытаскиваю инфу из БД для графика -  Пользователи с наибольшим количеством лайков
        user_countlikes = Choice.objects.values ('id_user').annotate (total=Sum ('likes_count'))
        user1 = []
        count1 = []
        for user_count in user_countlikes:
            user1.append (user_count ['id_user'])
            count1.append ((user_count ['total']))

        fig = plt.figure ()
        ax_1 = fig.add_subplot (2, 2, 1)
        ax_2 = fig.add_subplot (2, 2, 2)

        ax_1.set (title='Пользователи с наибольшим количеством комментариев',xlabel='id пользователей',
                  ylabel='Кол-во комментариев')
        ax_2.set (title='Пользователи с наибольшим количеством лайков', xlabel='id пользователей',
                  ylabel='Кол-во лайков')
        ax_1.bar(user,count)
        ax_2.bar(user1,count1)
        plt.show ()

        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})
    else:
        domainform = DomainForm ()
        return render (request, "index.html", {"form": domainform})