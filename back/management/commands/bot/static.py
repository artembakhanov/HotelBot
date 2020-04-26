from enum import Enum

from telebot.types import *

from back.models import Booking

HOTEL_INFO = "ℹ️ Hotel Info"
MY_BOOKINGS = "📖 My Bookings"

MAIN_MENU = ReplyKeyboardMarkup(one_time_keyboard=True)
MAIN_MENU.row(HOTEL_INFO, MY_BOOKINGS)


def BOOKING_BUTTONS(booking_id):
    keyboard = InlineKeyboardMarkup()
    booking_message_button = InlineKeyboardButton("ℹ️ Contact us", callback_data=f"h_{booking_id}")
    cancel_booking_button = InlineKeyboardButton("❌ Cancel", callback_data=f"c_{booking_id}")
    keyboard.add(booking_message_button)
    if Booking.objects.get(id=booking_id).active:
        keyboard.add(cancel_booking_button)
    return keyboard


def HOTEL_BUTTONS(hotel):
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton("WebSite", url=hotel.website)
    hotel_message_button = InlineKeyboardButton("ℹ️ Contact us", callback_data=f"h_")
    keyboard.add(url_button)
    keyboard.add(hotel_message_button)

    return keyboard


class State(Enum):
    DEFAULT = 0
    BOOKING_CODE = 1
    QUESTION_ANSWER = 2
