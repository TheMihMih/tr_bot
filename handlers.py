from glob import glob
from random import choice
import ephem
from datetime import datetime
from util import get_smile, main_keybord, play_random_numbers

def greeting(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Кукусики {context.user_data['emoji']}",
        reply_markup=main_keybord()
    )


def talking(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_name = update.effective_user.first_name
    user_text = update.message.text
    update.message.reply_text(
        f"Привет, {user_name}{context.user_data['emoji']}. Ты ввел {user_text}",
        reply_markup=main_keybord()
    )


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(ValueError, TypeError):
            message = 'Введите целое число'
    else:
        message = 'Введите целое число'
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keybord())


def full_moon(update, context):
    fullmoon = ephem.next_full_moon(datetime.now())
    update.message.reply_text(fullmoon, reply_markup=main_keybord())


def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f'Ваши координаты {coords} {context.user_data["emoji"]}',
        reply_markup = main_keybord()
    )
