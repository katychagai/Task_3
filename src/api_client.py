import requests
from .config import get_settings
from .urls import REGISTER_URL, LOGIN_URL, USER_URL

#API клиент для работы с пользователями Stellar Burgers
#Создает пользователя через API
def register_user(payload):
    return requests.post(f"{get_settings().base_url}{REGISTER_URL}", json=payload)

#Авторизует пользователя через API
def login_user(payload):
    return requests.post(f"{get_settings().base_url}{LOGIN_URL}", json=payload)

#Удаляет пользователя через API
def delete_user(token):
    if not token:
        return None
    headers = {"Authorization": token}
    return requests.delete(f"{get_settings().base_url}{USER_URL}", headers=headers)

