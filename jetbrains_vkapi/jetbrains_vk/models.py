from django.db import models

#from jetbrains_vk.models import Choice

class Choice(models.Model):
    id_user = models.CharField(max_length=20)
    likes_count = models.IntegerField()
    date = models.CharField(max_length=20)