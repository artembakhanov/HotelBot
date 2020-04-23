import telebot
from django.conf import settings
from django.core.management.base import BaseCommand
from . import bot


class Command(BaseCommand):
    help = "Run the bot"

    def handle(self, *args, **options):
        bot.main()
