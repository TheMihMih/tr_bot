# Проект CatBot 

CatBot - присылает котиков

## Установка 

1. Клонируйте репозиторий 
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте  файл `settings.py`
5. Впишите в settings.py переменные:
```
API_KEY = "API ключ для бота"
PROXY_URL = "Адрес прокси"
PROXY_USERNAME = "Логин на прокси"
PROXY_PASSWORD = "Пароль на прокси"
USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']
```
6. Запустите бота коммандной `python bot.py`