from glob import glob
import os
from random import choice
from datetime import datetime
from db import db_session
from jobs import alarm
from util import (
    has_object_on_image,
    main_keyboard,
    play_random_numbers,
    get_bot_number,
    cat_rating_inline_keyboard,
    get_or_create_user,
    save_cat_image_vote,
    get_image_rating,
    user_voted,
    subscribe_user,
    unsubscribe_user,
    make_emodji,)


def greet_user(update, context) -> None:
    user = get_or_create_user(db_session, update.effective_user, update.message.chat.id)
    print("Вызван /start")
    update.message.reply_text(
        f"Здравствуй, пользователь!{make_emodji(user)}",
        reply_markup=main_keyboard(),
    )


def talk_to_me(update, context) -> None:
    user = get_or_create_user(db_session, update.effective_user, update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text}{make_emodji(user)}", reply_markup=main_keyboard())


def guess_number(update, context) -> None:
    user = get_or_create_user(db_session, update.effective_user, update.message.chat.id)
    if context.args:
        try:
            user_number = int(context.args[0])
            bot_number = get_bot_number(user_number)
            message = play_random_numbers(user_number, bot_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = f"Введите число {make_emodji(user)}"
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_cat_picture(update, context) -> None:
    user = get_or_create_user(db_session, update.effective_user, update.message.chat.id)
    cat_photo_list = glob("images/cat*.jp*g")
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    if user_voted(cat_photo_filename, user.user_id):
        rating = get_image_rating(cat_photo_filename)
        keyboard = None
        caption = f"Рейтинг картинки {rating}"
    else:
        keyboard = cat_rating_inline_keyboard(cat_photo_filename)
        caption = None
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_photo_filename, "rb"),
        reply_markup=keyboard,
        caption=caption,
    )


def user_coordinates(update, context) -> None:
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords}!", reply_markup=main_keyboard()
    )


def check_user_photo(update, context) -> None:
    update.message.reply_text("Обрабатываем фотографию")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    cat_photo_list = glob("images/cat*.jp*g")
    if has_object_on_image(file_name, "cat"):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку")
        new_filename = os.path.join(
            "images",
            f"cat_{str(len(cat_photo_list) + 1) + datetime.now().strftime('_%d%m%Y_%H%M%S')}.jpg",
        )
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text("Тревога, котик на фото не обнаружен")
        os.remove(file_name)


def subscribe(update, context) -> None:
    user = get_or_create_user(db_session, update.effective_user, update.message.chat.id)
    subscribe_user(db_session, user)
    update.message.reply_text(f"Вы успешно подписались{make_emodji(user)}")


def unsubscribe(update, context) -> None:
    user = get_or_create_user(db_session, update.effective_user, update.message.chat.id)
    unsubscribe_user(db_session, user)
    update.message.reply_text("Вы успешно отписались")


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f"Уведомление через {alarm_seconds} секунд")
    except (ValueError, TypeError):
        update.message.reply_text("Введите целое число секунд после команды")


def cat_picture_rating(update, context) -> None:
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split("|")
    vote = int(vote)
    user = get_or_create_user(
        db_session, update.effective_user, update.effective_chat.id
    )
    save_cat_image_vote(db_session, user, image_name, vote)
    rating = get_image_rating(image_name)
    update.callback_query.edit_message_caption(caption=f"Рейтинг картинки {rating}")
