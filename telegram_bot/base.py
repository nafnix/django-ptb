from telegram.ext import Application, ContextTypes

from config._settings import django_settings
from telegram_bot.utils import CustomContext


# Set up PTB application and a web application for handling the incoming requests.

context_types = ContextTypes(context=CustomContext)
# Here we set updater to None because we want our custom webhook server to handle the updates
# and hence we don't need an Updater instance
ptb_application = (
    Application.builder()
    .token(django_settings.TELEGRAM_TOKEN)
    .context_types(context_types)
    .build()
)
