import json

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators import csrf
from telegram import Update

from telegram_bot.base import ptb_application


@csrf.csrf_exempt
async def telegram(request: HttpRequest) -> HttpResponse:
    """Handle incoming Telegram updates by putting them into the `update_queue`"""
    await ptb_application.update_queue.put(
        Update.de_json(data=json.loads(request.body), bot=ptb_application.bot)
    )
    return HttpResponse()


@csrf.csrf_exempt
async def custom_updates(request: HttpRequest) -> HttpResponse:
    """
    Handle incoming webhook updates by also putting them into the `update_queue` if
    the required parameters were passed correctly.
    """
    try:
        user_id = int(request.GET['user_id'])
        payload = request.GET['payload']
    except KeyError:
        return HttpResponseBadRequest(
            'Please pass both `user_id` and `payload` as query parameters.',
        )
    except ValueError:
        return HttpResponseBadRequest('The `user_id` must be a string!')

    await ptb_application.bot.send_message(user_id, f'你好!{str(payload)}')
    return HttpResponse('做到了!')


@csrf.csrf_exempt
async def health(_: HttpRequest) -> HttpResponse:
    """For the health endpoint, reply with a simple plain text message."""
    return HttpResponse('The bot is still running fine :)')
