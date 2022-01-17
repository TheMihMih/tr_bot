from random import randint, choice
from emoji import emojize
from settings import USER_EMOJI
from telegram import ReplyKeyboardMarkup, KeyboardButton



def get_smile(user_data):
    if 'emoji' not in user_data:   
        smile = choice(USER_EMOJI)
        return emojize(smile, use_aliases = True)
    return user_data['emoji']


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif bot_number==user_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message


def main_keybord():
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])
