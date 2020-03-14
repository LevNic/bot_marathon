import re

from datetime import datetime, timedelta, time
from dateutil import rrule

from data_graph import graph_creator, data_for_graph, series_list_creator
from messages_from_graph import GraphMessages
from vk_metod import VkMethod
from file_manager import FileManager

class Vk_bot:
    def __init__(self, user_id):
        self.method = VkMethod()
        self.incoming_message = {}
        self.text = '_NO_'
        self.user_id = user_id
        self.name = self.method.get_user_name(self.user_id)
        self.graph = graph_creator(data_for_graph)
        self.message = GraphMessages(self.name, self.graph)
        # Стартовый этап всегда должен называться hello
        self.real_step_graph = 'hello'
        self.series_list = series_list_creator()
        # Стартовый payload всегда
        self.payload = '["undefinited"]'
        self.manager = FileManager()

    # Отправляет сообщение с вложением картинки(не аудио) если оно есть
    def post_all(self, get_message):
        if get_message['attachment']:
            self.method.send_image(self.user_id, get_message['attachment'])
        self.method.send_message(self.user_id, get_message['message'], get_message['keyboard'])

    # Отправляет серию сообщений с заданным интервалом
    # Предварительно проверяем наличие обновлений
    def series(self):
        print('ВЫЗВАЛИ СЕРИЮ')
        get_message = self.series_preparation()
        list_rrule = self.list_rrule()
        step = 0
        for item in list_rrule:
            new_structure = self.manager.run_manager()
            if len(new_structure) > 0:
                self.graph = graph_creator(new_structure)
                get_message = self.series_preparation()
            print('TIME RRULE', item)
            print('NOW_DATE', datetime.now())
            delta = item - datetime.now()
            print('DELTA', delta)
            second = delta.total_seconds()
            print('DELTA SECONDS', second)
            while second > 0:
                delta = item - datetime.now()
                second = delta.total_seconds()
            print(f'STEP {step} OF {len(list_rrule)}')
            self.post_series_graph(step, get_message)
            step += 1
    
    # Подготавливаем данные для отправки серии сообщений
    def series_preparation(self):
        print('SERIES DATA PREPARATION STARTED')
        series_list = self.series_list
        message = GraphMessages(self.name, self.graph)
        get_message = message.get_all(series_list)
        return get_message

    def list_rrule(self):
        if datetime.now().time().hour > 13:
            print('+ 1 DAY')
            d = datetime.now().date() + timedelta(days=1)
        else:
            d = datetime.now().date()
        t = time(13, 10)
        start = datetime.combine(d, t)  
        print('TIME START SERIES', start)
        list_rrule = list(rrule.rrule(rrule.MINUTELY, count=len(self.series_list), dtstart=start))
        return list_rrule

    # Отправляет серию сообщений с заданным интервалом на основе графа
    def post_series_graph(self, step, get_message):
        print('*' * 50)
        self.post_all(get_message[self.series_list[step]])
        self.real_step_graph = self.series_list[step]

    def speaker_for_graph(self):
        print('SREAKER WORK')
        pattern = re.compile(r'\w+_?\d*')
        # 'Определяем предстоящие шаги бота'
        print('PAYLOAD FOR ...', self.payload, type(self.payload))
        if self.payload != '["undefinited"]':
            
            payload = re.findall(pattern, self.payload)
            print('PAYLOAD IN SPEAKER', payload, type(payload))
            self.real_step_graph = payload[0]

        print('ТЕКУЩИЙ ЭТАП', self.real_step_graph)
        message = GraphMessages(self.name, self.graph)
        get_message = message.get_one_message(self.real_step_graph)
        #print('SPEAKER MESSAGE', get_message)
        self.post_all(get_message)
