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
    state = models.PositiveSmallIntegerField(default=0)


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

    def __str__(self):
        return f"Room \"{self.name}\""


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    confirmation_number = models.CharField(max_length=8, validators=[
        RegexValidator('[0-9]{8}', message="It should be eight digits.")])
    date_check_in = models.DateTimeField()
    date_check_out = models.DateTimeField()
    active = models.BooleanField(default=True, auto_created=True)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    message_id = models.IntegerField()