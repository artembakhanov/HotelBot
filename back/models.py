from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Hotel(models.Model):
    name = models.TextField()
    admin_telegram_id = models.IntegerField()
    website = models.URLField()

    def __str__(self):
        return f"Hotel \"{self.name}\""


class User(models.Model):
    telegram_id = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    username = models.TextField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=1)


class HotelInfo(models.Model):
    button_name = models.TextField()
    content = models.TextField()


class RoomCategory(models.Model):
    class Meta:
        verbose_name_plural = "Room categories"

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.TextField()
    min_price = models.PositiveIntegerField()


class Room(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.PROTECT)
    name = models.TextField()


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    confirmation_number = models.TextField(validators=[RegexValidator("[0-9]{8}")])
    date_check_in = models.DateTimeField()
    date_check_out = models.DateTimeField()
    active = models.BooleanField(default=False, auto_created=True)
