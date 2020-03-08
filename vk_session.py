# Класс сессии бота для работы с  ВК

import vk_api.vk_api

#from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config_bot import vk_token as TOKEN
from config_bot import vk_grour_id as ID


class VkSession:

    def __init__(self):
        # Авторизируемся как сообщество
        self.vk_session = vk_api.VkApi(token=TOKEN)
        # Тип сообщения - "Новое"
        self.message_new = VkBotEventType.MESSAGE_NEW

    # Методы АПИ(позволяет обращаться к методам ВК)
    def vk_method(self):
        return self.vk_session.get_api()

    # Создаем экземпляр сервера для группы
    def longpoll(self):
        return VkBotLongPoll(self.vk_session, ID)