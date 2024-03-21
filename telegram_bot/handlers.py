import html

from telegram import Update
from telegram.constants import ParseMode

from config._settings import django_settings
from constants import WEBHOOK_URL
from telegram_bot.utils import CustomContext, WebhookUpdate


async def start(update: Update, context: CustomContext) -> None:
    """Display a message with instructions on how to use this bot."""
    payload_url = html.escape(
        f'{WEBHOOK_URL}/submitpayload?user_id={update.effective_user.id}&payload=example'
    )
    text = (
        f'Your ID is <code>{update.effective_user.id}</code>'
        f'To check if the bot is still running, call <code>{WEBHOOK_URL}/healthcheck</code>.\n\n'
        f'To post a custom update, call <code>{payload_url}</code>.'
    )
    await update.message.reply_html(text=text)  # type: ignore


async def webhook_update(update: WebhookUpdate, context: CustomContext) -> None:
    """Handle custom updates."""
    chat_member = await context.bot.get_chat_member(chat_id=update.user_id, user_id=update.user_id)
    payloads = context.user_data.setdefault('payloads', [])  # type: ignore
    payloads.append(update.payload)
    combined_payloads = '</code>\n• <code>'.join(payloads)
    text = (
        f'The user {chat_member.user.mention_html()} has sent a new payload. '
        f'So far they have sent the following payloads: \n\n• <code>{combined_payloads}</code>'
    )
    await context.bot.send_message(
        chat_id=django_settings.TELEGRAM_ADMIN_CHAT_ID, text=text, parse_mode=ParseMode.HTML
    )
