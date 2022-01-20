from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_anketa
from util import main_keyboard


def anketa_start(update, context):
    update.message.reply_text(
        "Привет, как Вас зовут",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"


def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text(
            "Введите корректное имя и фамилию",
        )
        return "name"
    else:
        context.user_data["anketa"] = {"name": user_name}
        reply_keyboard = [['1', '2', "3", '4', '5']]
        update.message.reply_text(
            "Пожалуйста оцените нашего бота от 1 до 5",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, resize_keyboard=True, one_time_keyboard=True
            )
        )
        return "rate"


def anketa_rating(update, context):
    context.user_data['anketa']['rating'] = int(update.message.text)
    update.message.reply_text(
        "Напишите комментарий, или нажмите /skip"
    )
    return 'comment'


def anketa_skip(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
    )
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(
        user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def anketa_comment(update, context):
    context.user_data['anketa']['comment'] = update.message.text
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
    )
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(
        user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f'''<b>Имя Фамилия</b>: {anketa["name"]}
<b>Оценка</b>: {anketa['rating']}
'''
    if 'comment' in anketa:
        user_text += f'\n<b>Комментарий</b>: {anketa["comment"]}'

    return user_text


def anketa_dunno(update, context):
    update.message.reply_text("ТЫ ЧЕ ОТПРАВИЛ, СУКАПАДЛА? ВВОДИ НОРМАЛЬНО")
