# Сервер для работы с ВК
import threading

from vk_session import VkSession
from vk_metod import VkMethod
from bot import Vk_bot


class VkServer:
    vs = VkSession()
    method = VkMethod()
    
    def __init__(self):
        # Словарь для сессий бота
        self.bot = {}
        # Словарь для сообщений по времени
        self.third_series = {}
        self.user_id = 0
        self.longpoll = self.vs.longpoll()
        self.message_new = self.vs.message_new
    
        # Основной цикл
    def listen(self):
        print('SERVER STARTED')
        for event in self.longpoll.listen():
            print('LISTEN')
            if event.type == self.message_new:
                message = event.object.message
                #client_info = event.object.client_info
                if message['id'] > 0:
                    self.user_id = message['from_id']
                    print('ID пользователя:', self.user_id)
                else:
                    self.user_id = message['peer_id']
                    print('Это сообщение из группы')
                # Если сессии бота с usr_id нет в словаре, то добавим,
                if self.user_id not in self.bot:
                    #print('БОТ ЗАПИСАН')
                    self.bot[self.user_id] = Vk_bot(self.user_id)        
                # Передадим в Бота текст сообщения.
                self.bot[self.user_id].incoming_message = message
                self.bot[self.user_id].text = message['text']
                # Если в сообщении есть payload то передаем его в бот
                if 'payload' in message.keys():
                    self.bot[self.user_id].payload = message['payload']
                    #print('PAYLOAD IN SERVER', message['payload'])

                # Создаем параллельный поток, если его нет
                if self.user_id not in self.third_series:
                    self.third_series[self.user_id] = threading.Thread(target=self.bot[self.user_id].series, daemon=False)
                    print('ВЫЗЫВАЕМ СЕРИЮ')
                    self.third_series[self.user_id].start()
                print('*' * 52)

                # Запускаем диалог
                self.bot[self.user_id].speaker_for_graph()
  
