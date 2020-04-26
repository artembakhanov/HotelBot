from enum import Enum

from telebot.types import *

HOTEL_INFO = "ℹ️ Hotel Info"
MY_BOOKINGS = "📖 My Bookings"

MAIN_MENU = ReplyKeyboardMarkup(one_time_keyboard=True)
MAIN_MENU.row(HOTEL_INFO, MY_BOOKINGS)


def BOOKING_BUTTONS(booking_id):
    keyboard = InlineKeyboardMarkup()
    booking_message_button = InlineKeyboardButton("ℹ️ Contact us", callback_data=f"h_{booking_id}")
    keyboard.add(booking_message_button)
    return keyboard


class State(Enum):
    DEFAULT = 0
    BOOKING_CODE = 1
