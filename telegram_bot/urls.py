from django.urls import path

from telegram_bot.views import custom_updates, health, telegram


urlpatterns = [
    path('telegram', telegram, name='Telegram updates'),
    path('submitpayload', custom_updates, name='custom updates'),
    path('healthcheck', health, name='health check'),
]
