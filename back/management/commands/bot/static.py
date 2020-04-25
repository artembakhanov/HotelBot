from enum import Enum

from telebot.types import *


HOTEL_INFO = "Hotel Info"
MY_BOOKINGS = "My Bookings"

MAIN_MENU = ReplyKeyboardMarkup(one_time_keyboard=True)
MAIN_MENU.row(HOTEL_INFO, MY_BOOKINGS)


class State(Enum):
    DEFAULT = 0
    BOOKING_CODE = 1
