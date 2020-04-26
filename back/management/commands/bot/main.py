import re

import telebot

from HotelManagementBot import settings
from back.models import User as User_, Hotel, Question
from .static import *
from .wrappers import save_user

HOTEL_ID = 1  # this was asked to be const


def main():
    bot = telebot.TeleBot(settings.TOKEN)

    question_states = {}

    @bot.message_handler(commands=['start'])
    @save_user
    def start(m, user):
        bot.send_message(m.chat.id,
                         f"Hello, {user.first_name}! Welcome to the Hotel Management Bot. Use the menu keyboard below to navigate.\n"
                         f"For now your account is attached to Hotel 1.",
                         reply_markup=MAIN_MENU)

    @bot.message_handler(content_types=['text'], func=lambda m: m.text == MY_BOOKINGS)
    @save_user
    def see_booking(m, user):
        bot.send_message(m.chat.id, "Please, enter your booking id and confirmation code.")
        user.state = State.BOOKING_CODE.value
        user.save()

    @bot.message_handler(content_types=['text'], func=lambda m: m.text == HOTEL_INFO)
    @save_user
    def hotel_info(m, user):
        hotel = Hotel.objects.get(id=HOTEL_ID)
        bot.send_message(m.chat.id,
                         f"*{hotel.name}*\n\n",
                         reply_markup=HOTEL_BUTTONS(hotel))

    @bot.message_handler(content_types=['text'],
                         func=lambda m: User_.objects.get(telegram_id=m.from_user.id).state == State.BOOKING_CODE.value)
    @save_user
    def provide_hotel_info(m, user):
        match = re.fullmatch(r'([0-9]+)\s+([0-9]{8})', m.text)
        if match:
            booking_id, confirmation_code = match.groups()
            try:
                booking = Booking.objects.get(id=booking_id, confirmation_number=confirmation_code)
                sym = "" if booking.active else "~"
                bot.send_message(
                    m.chat.id,
                    f"📖 {sym}Booking{sym} *\\#{booking.id}*\n\n"
                    f"🛏 Room: {booking.room.name}\n"
                    f"{'✅ The booking is active' if booking.active else '❌ The booking is cancelled'}",
                    parse_mode="MarkdownV2",
                    reply_markup=BOOKING_BUTTONS(booking.id)
                )
                user.state = State.DEFAULT.value
                user.save()
            except Booking.DoesNotExist:
                bot.send_message(m.chat.id, "The booking with such id and the confirmation code does not exist.\n"
                                            "Please try again.")
        else:
            bot.send_message(m.chat.id,
                             "The message has incorrect format. Firstly, put booking id and then confirmation code.")

    @bot.message_handler(content_types=['text'],
                         func=lambda m: User_.objects.get(
                             telegram_id=m.from_user.id).state == State.QUESTION_ANSWER.value)
    @save_user
    def send_question(m, user):
        user.state = State.DEFAULT.value
        user.save()

        text = m.text
        q = question_states[m.from_user.id]
        if q['booking_id'] is None:
            booking = None
        else:
            booking = Booking.objects.get(id=q['booking_id'])

        question = Question(user=user, booking=booking, content=text)
        question.save()
        message = bot.send_message(q["admin"],
                                   f"⚠️ New Question \\#{question.id}\n"
                                   f"\\[Booking \\#{q['booking_id']}\\]\n\n"
                                   f"_{text}_\n\n"
                                   f"*Please reply to this message with your answer*\\.", parse_mode="MarkdownV2")

        question.message_id = message.message_id
        question.save()

        del q

        bot.send_message(m.chat.id, f"✅ Your question #{question.id} is sent to the admin.\n"
                                    f" You will get the answer soon.",
                         reply_markup=MAIN_MENU)

    @bot.message_handler(content_types=['text'],
                         func=lambda m: m.reply_to_message and Question.objects.get(
                             message_id=m.reply_to_message.message_id))
    def write_answer(m):
        answer = m.text

        question = Question.objects.get(message_id=m.reply_to_message.message_id)
        question.answer = answer
        question.save()

        booking_text = f"regarding your booking *\\#{question.booking.id}*" if question.booking else ""
        bot.send_message(question.user.telegram_id,
                         f"✅ You got an answer to question *\\#{question.id}* {booking_text}\n\n"
                         f"_{answer}_",
                         parse_mode="MarkdownV2")

    @bot.callback_query_handler(func=lambda call: call.data[:2] == "h_")
    def write_message_booking(call):
        booking_id = call.data[2:]
        if booking_id == "":
            booking_id = None
        admin = Hotel.objects.get(id=HOTEL_ID).admin_telegram_id

        question_states[call.from_user.id] = {"booking_id": booking_id, "admin": admin}

        print(call.from_user.id)
        user = User_.objects.get(telegram_id=call.from_user.id)

        user.state = State.QUESTION_ANSWER.value
        user.save()

        bot.send_message(call.message.chat.id, f"Please, state your question in the next message.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    @bot.callback_query_handler(func=lambda call: call.data[:2] == "c_")
    def write_message_booking(call):
        booking_id = call.data[2:]
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.active = False
            booking.save()
            sym = "" if booking.active else "~"
            bot.edit_message_text(f"📖 {sym}Booking{sym} *\\#{booking.id}*\n\n"
                                  f"🛏 Room: {booking.room.name}\n"
                                  f"{'✅ The booking is active' if booking.active else '❌ The booking is cancelled'}",
                                  parse_mode="MarkdownV2",
                                  reply_markup=BOOKING_BUTTONS(booking.id),
                                  message_id=call.message.message_id,
                                  chat_id=call.message.chat.id)
            bot.answer_callback_query(call.id, "Cancelled!")
        except Booking.DoesNotExist:
            pass

    bot.polling()
