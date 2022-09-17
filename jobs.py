from datetime import datetime
from telegram.error import BadRequest
from db import db_session
from util import get_subscribed


def send_upds(context):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:S")
    for user in get_subscribed(db_session):
        try:
            context.bot.send_message(chat_id=user.chat_id, text=f"Точное время {now}")
        except BadRequest:
            print(f"Chat {user.chat_id} not found")


def alarm(context):
    context.bot.send_message(
        chat_id=context.job.context,
        text='АЛЛО, СУКА, ЭТО ВОССТАНИЕ МАШИН'
    )
