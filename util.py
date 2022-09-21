from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from datetime import datetime
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize

from models import User, Anketa, ImagesRating
import settings


def get_bot_number(user_number: int) -> int:
    return randint(user_number - 10, user_number + 10)


def play_random_numbers(user_number: int, bot_number: int) -> str:
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, мое {bot_number}, вы проиграли"
    return message


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [['Прислать котика', KeyboardButton('Мои координаты', request_location=True), 'Заполнить анкету']],
        resize_keyboard=True
    )


def has_object_on_image(file_name: str, object_name: str) -> bool:
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(image=image)
            )
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response, object_name)


def check_response_for_object(response, object_name: str) -> bool:
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.9:
                return True
    else:
        print(f'Ошибка распознования картинки {response.outputs[0].status.details}')

    return False


def cat_rating_inline_keyboard(image_name: str) -> InlineKeyboardMarkup:
    callback_text = f"rating|{image_name}|"
    keyboard = [
        [
            InlineKeyboardButton('Нравится', callback_data=callback_text + '1'),
            InlineKeyboardButton('Не нравится', callback_data=callback_text + '-1')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_or_create_user(db_session, effective_user, chat_id: int) -> User:
    user = User.query.filter_by(user_id=effective_user.id).first()
    if not user:
        user = User(
            user_id=effective_user.id,
            first_name=effective_user.first_name,
            last_name=effective_user.last_name,
            username=effective_user.username,
            chat_id=chat_id,
            emoji=choice(settings.USER_EMOJI),
            subscribed=False,
        )
        db_session.add(user)
        db_session.commit()
    return user


def save_anketa(db_session, user_id, anketa_data) -> None:
    anketa = Anketa.query.filter_by(user_id=user_id).first()
    anketa_data['created'] = datetime.now()
    if not anketa:
        anketa = Anketa(
            user_id=user_id,
            **anketa_data
        )
        db_session.add(anketa)
    else:
        anketa.update(**anketa_data)

    db_session.commit()


def subscribe_user(db_session, user) -> None:
    if not user.subscribed:
        user.subscribed = True
        db_session.commit()


def unsubscribe_user(db_session, user) -> None:
    user.subscribed = False
    db_session.commit()


def get_subscribed() -> User:
    return User.query.filter(User.subscribed.is_(True))


def save_cat_image_vote(db_session, user_data, image_name: str, vote: int) -> None:
    user_id = user_data.user_id
    image = ImagesRating.query.filter_by(image_name=image_name).first()

    if not image:
        image = ImagesRating(
            image_name=image_name,
            votes={user_id: vote},
        )
        db_session.add(image)
        db_session.commit()
    elif not user_voted(image_name, user_id):
        image.votes[user_id] = vote
        db_session.commit()


def user_voted(image_name: str, user_id) -> bool:
    image = ImagesRating.query.filter_by(image_name=image_name).first()
    if image and image.votes.get(user_id):
        return True
    return False


def get_image_rating(image_name: str) -> int:
    image_to_rate = ImagesRating.query.filter_by(image_name=image_name).first()
    rating = sum([rate for user, rate in image_to_rate.votes.items()])
    return rating


def make_emodji(user: User):
    return emojize(user.emoji, use_aliases=True)
