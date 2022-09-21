from datetime import datetime
from telegram.error import BadRequest
from util import get_subscribed


def send_upds(context) -> None:
    now = datetime.now().strftime("%d.%m.%Y %H:%M:S")
    for user in get_subscribed():
        try:
            context.bot.send_message(chat_id=user.chat_id, text=f"Точное время {now}")
        except BadRequest:
            print(f"Chat {user.chat_id} not found")


def alarm(context) -> None:
    context.bot.send_message(
        chat_id=context.job.context,
        text='АЛЛО, СУКА, ЭТО ВОССТАНИЕ МАШИН'
    )
