from django.db import models


# Create your models here.
class User(models.Model):
    telegram_id = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    username = models.TextField()


class Hotel(models.Model):
    name = models.TextField()
    admin_telegram_id = models.IntegerField()
    website = models.URLField()
