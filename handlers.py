from glob import glob
from random import choice
import ephem
from datetime import datetime
from util import get_smile, main_keybord, play_random_numbers, has_obj_on_image
import os

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


def check_user_photo(update, context):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Файл сохранен")
    if has_obj_on_image(filename, "cat"):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, котик не обнаружен!")
