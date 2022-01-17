from email.mime import image
from importlib.metadata import metadata
from random import randint, choice
from urllib import request
from emoji import emojize
from settings import USER_EMOJI, CLARIFAI_API_KEY
from telegram import ReplyKeyboardMarkup, KeyboardButton
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2



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


def has_obj_on_image(file_name, obj_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (("authorization", f'Key {CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id = 'aaa03c23b3724a16a56b629203edc62c',
        inputs=[resources_pb2.Input(data=resources_pb2.Data(image=image))]
    )
    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_obj(response, obj_name)
    

def check_response_for_obj(response, obj_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == obj_name and concept.value >= 0.85:
                return True
    else:
        print(f"Ошибка распознавания картинки {response.outputs[0].status.details}")

    return False

def main_keybord():
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])
