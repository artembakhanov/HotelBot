from django.contrib import admin

# Register your models here.
from .models import User, Hotel, RoomCategory, Room, Booking


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'first_name', 'last_name')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin_telegram_id', 'website')


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("hotel", "name", "min_price")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_category", "name")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "confirmation_number", "active")
