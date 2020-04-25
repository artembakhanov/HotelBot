import re

import telebot

from HotelManagementBot import settings
from back.models import User as User_
from .static import *
from .wrappers import save_user

HOTEL_ID = 1  # this was asked to be const


def main():
    bot = telebot.TeleBot(settings.TOKEN, )

    @bot.message_handler(commands=['start'])
    @save_user
    def start(m, user):
        bot.send_message(m.chat.id,
                         f"Hello, {user.first_name}! Welcome to the Hotel Management Bot. Use the menu keyboard below to navigate.\n"
                         f"For now your account is attached to Hotel 1.",
                         reply_markup=MAIN_MENU)

    @bot.message_handler(content_types=['text'], func=lambda m: m.text == MY_BOOKINGS)
    @save_user
    def hotel_info(m, user):
        bot.send_message(m.chat.id, "Please, enter your booking id and confirmation code.")
        user.state = State.BOOKING_CODE.value
        user.save()

    @bot.message_handler(content_types=['text'],
                         func=lambda m: User_.objects.get(telegram_id=m.from_user.id).state == State.BOOKING_CODE.value)
    @save_user
    def provide_hotel_info(m, user):
        match = re.fullmatch(r'([0-9]+)\s+([0-9]{8})', m.text)
        if match:
            booking_id, confirmation_code = match.groups()
            bot.send_message(m.chat.id, "Here it should be your booking.")
            user.state = State.DEFAULT.value
            user.save()
            # send booking here
        else:
            bot.send_message(m.chat.id,
                             "The message has incorrect format. Firstly, put booking id and then confirmation code.")

    bot.polling()
