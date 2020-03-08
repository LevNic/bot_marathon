# Класс методов, которые будут использоваться при работе бота с ВК

import vk_api

from vk_api import VkUpload
from vk_api.utils import get_random_id

from vk_session import VkSession

class VkMethod:

    def __init__(self):
        # Создаем экземпляр сессии
        self.vs = VkSession()
        # Создаем обращение к методам АПИ ВК
        self.method = self.vs.vk_method()

    # Работа с картинками
    def upload(self):
       return VkUpload(self.vs.vk_session)

    # Определение иени пользователя
    def get_user_name(self, user_id):
        return self.method.users.get(user_id=user_id)[0]['first_name']

    # Отправка сообщения
    def send_message(self, user_id, text, keyboard):
        return self.method.messages.send(user_id=user_id, random_id=get_random_id(), message=text, keyboard=keyboard)

    # Отправка сообщения в групповом чате
    def send_message_group(self, send_id, text):
        self.method.messages.send(peer_id=send_id, message=text)
  
    # Отправка картинки
    def send_image(self, user_id, attachment):
        return self.method.messages.send(user_id=user_id, random_id=get_random_id(), attachment=attachment)

    # Определение даты рождения пользователя
    def get_user_bdate(self, user_id):
        return self.method.users.get(user_id=user_id, fields='bdate')
