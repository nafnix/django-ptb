import asyncio
import logging

from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import CommandHandler, TypeHandler

from constants import WEBHOOK_URL
from telegram_bot.base import ptb_application
from telegram_bot.handlers import start, webhook_update
from telegram_bot.utils import WebhookUpdate


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# register handlers
ptb_application.add_handler(CommandHandler('start', start))
ptb_application.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))


class Command(BaseCommand):
    help = 'Run Telegram Bot'

    def handle(self, *args, **options):
        # Run application and webserver together
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            ptb_application.bot.set_webhook(
                url=f'{WEBHOOK_URL}telegram', allowed_updates=Update.ALL_TYPES
            ),
        )

        ptb_application.run_polling(allowed_updates=Update.ALL_TYPES)
