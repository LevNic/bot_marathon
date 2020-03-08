import re

from make_keyboard import Keyboards
from make_text import TextPreparation
from make_img import ImagesFile
from data_graph import series_list

# Класс сообщения
class GraphMessages:
    # Имя пользователя
    name = 'Uno'    
    # Словарь для записи параметров сообщения
    message = {}
    messages = {}
    pattern_key = re.compile(r'text_key_\d+_?\d*')
    pattern_type_key = re.compile(r'type_key_\d+_?\d*')
    
    def __init__(self, name, graph):

        #Экземпляр графа
        self.graph = graph
        # Имя пользователя
        self.name = name
        # Элземпляр класса клавиатуры
        self.keyboard = Keyboards()
        # Экземпляр класса картинки
        self.img = ImagesFile()
        # Экземпляр класса текста
        self.text_preparation = TextPreparation(self.name)
        # Название сообщения
        self.step = 'hello'

    # Ошибка
    def get_error(self):
        self.message['message'] = 'Опаньки!'
        self.message['keyboard'] = self.keyboard.del_key()
        self.message['attachment'] = 0
        return self.message

    # Сообщения на всех этапах бота
    def get_all(self, steps_list):
        print('GET ALL STARTED')
        messages = {}
        
        for steps in steps_list:
            print('*' * 50)
            print('STEP IN STEP LIST', steps)
            messages[steps] = self.get_one_message(steps)
        return messages

    # Сообщения на каждом этапе бота
    def get_one_message(self, step):
        print('GET ONE MESSAGE STARTED')
        message = {}
        text = self.graph.vertexes[step]['text'][0]
        text = self.text_preparation.send_name(text)
        message['message'] = text
        img = self.graph.vertexes[step].get('img')
        if img:
            message['attachment'] = self.img.attachment_for_graph(img)
        else:
            message['attachment'] = 0
        # Определяем количество кнопок и текст на них
        keys = []
        list_keys = self.graph.vertexes[step].keys()

        # Определяем есть ли от вершины ответвления
        list_edges = self.graph.edges[step]
        # Определяем есть ли данный этап в заглавном списке   
        if step in series_list:
            inline = True
        else:
            inline = False   
        # Создаем список с параметрами для payload кнопок
        payload = []
        if list_edges:    
            for i in range(0, len(list_edges)):
                if list_edges[i] not in series_list:
                    payload.append(list_edges[i])
                    print('PAYLOAD IN GET ONE MESSAGE BEGIN', payload)
            
        for key in list_keys:
            name_keys = re.findall(self.pattern_key, key)
            if name_keys:
                keys.append(self.graph.vertexes[step][name_keys[0]])
        print('KEYS', keys)
        print('PAYLOAD IN GET ONE MESSAGE', payload)
        message['keyboard'] = self.keyboard.create_keyboard_from_graph(keys, payload, inline)

        return message
