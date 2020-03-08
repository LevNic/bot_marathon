# Создание клавиатур

import json
from pprint import pprint
from copy import deepcopy

from data_graph import series_list

class Keyboards:
    
    def __init__(self):
        # Стандартная клавиша
        self.key = {"one_time": False, "inline": False,
        "buttons": 
            [
                [
                    {
                        "action": {"type": "text", "payload": "{\"0\": \"undefinited\"}", "label": "👋🏻 Привет"},
                        "color": "primary"
                    }
                ]
            ]
        }
        # Элемент клавифтуры
        self.elem_key = [{
                        "action": {"type": "text", "payload": "{\"0\": \"undefinited\"}", "label": "NO LABEL"},
                        "color": "primary"
                    }
                    ]
        # Удаление клавиатуры
        self.zero_key = {"buttons": [],"one_time": True}

    # Создание клавиши
    def get_key(self):
        return json.dumps(self.key)

    # def del_key(self):
    #     return json.dumps(self.zero_key)
    def del_key(self):
        return open('Keyboards/keyboard_del.json', 'r', encoding='UTF-8').read()
        

    # Создание ссылки на файл клавиатуры
    def link_keyboard(self, type_keyboard):
        return f'Keyboards/{type_keyboard}.json'

    # Получение клавиатуры из файла
    def get_keyboard_file(self, type_keyboard):
        keyboard_file = self.link_keyboard(type_keyboard)
        return open(keyboard_file, 'r', encoding='UTF-8').read()

    # Создание клавиатуры из графа (передаем список текстов кнопок 
    # и список переходов по кнопкам на другие ветки)
    def create_keyboard_from_graph(self, keys_list, payload, inline):
        print('STARTED create_keyboard_from_graph')
        #print('KEYS LIST', keys_list)
        # Если количество кнопок меньше, чем количество переходов,
        # добавляем количество кнопок и присваиваем им текст с названием перехода
        if len(keys_list) >= 1 and len(payload) > len(keys_list):
            delta = len(payload) - len(keys_list)
            #print('DELTA', delta)
            for i in range(delta, 0, -1):
                #print('I', i)
                keys_list.append(payload[len(payload) - i])
        # Если кнопок нет, то убираем клавиатуру
        if len(keys_list) == 0:
            copy_key = deepcopy(self.zero_key)
        # Если кнопка одна и переход на новую ветку один,
        # присваиваем кнопке этот переход
        elif len(keys_list) == 1 and len(payload) == 1:
            print('KEYS LIST 1', keys_list)
            # Создаем копию шаблонной кнопки
            copy_key = deepcopy(self.key)
            print('COPY KEY 1', copy_key)
            # Создаем на кнопке текст из списка кнопок
            copy_key['buttons'][0][0]['action']['label'] = keys_list[0]
            # Создаем пустой словарь для записи названия перехода
            payload_dict = []
            # Записываем нулевой элемент
            payload_dict.append(payload[0])
            # Вызываем функцию меняющую payload в кнопках
            self.update_payload(payload_dict, copy_key)
            #print('KEYBOARD', copy_key)
        # В случае, если кнопок больше 1
        else:
            copy_key = deepcopy(self.key)
            # Для первой кнопки
            copy_key['buttons'][0][0]['action']['label'] = keys_list[0]
            # Цикл для остальных кнопок
            for n in range(1, len(keys_list)):
                # Создаем копию элемента кнопки 
                elem_key = deepcopy(self.elem_key)
                # Меняем текст на кнопке
                elem_key[0]['action']['label'] = keys_list[n]
                # Добавляем кнопку к клавиатуре
                copy_key['buttons'].append(elem_key)
            # print('KOPY KEY', copy_key['buttons'][0][0]['action']['payload'])
            # print('TYPE', type(copy_key['buttons'][0][0]['action']['payload']))
            self.update_payload(payload, copy_key)
        # Для заглавных кнопок этапа делаем кнопки inline
        if inline and copy_key != self.zero_key:
            copy_key['inline'] = True
        keyboard = json.dumps(copy_key)

        print('KEYBOARD CREATED')
        return keyboard

    
    def update_payload(self, payload, keys):
        print('STARTED update_payload')
        if payload:
            # payload_str = '{\\"0\\": \\"'+payload[0]+'\\"}'
            # print('PAYLOAD STR', payload_str)
            # print('PAYLOAD', payload)
            # print('LEN PAYLOAD', len(payload))
            if len(payload) == 1:
                for i in range(len(keys['buttons'])):
                    payload_str = '{\"0\": \"'+payload[0]+'\"}'
                    #print('PAYLOAD STR', payload_str)
                    #print('PAYLOAD', keys['buttons'][i][0]['action']['payload'])
                    keys['buttons'][i][0]['action']['payload'] = payload_str
                    #print('PAYLOAD NEW', keys['buttons'][i][0]['action']['payload'])
            elif len(payload) > 1 and len(payload) <= len(keys):
                # print('LEN PAYLOAD', len(payload))
                # print('LEN KEYS', len(keys))
                for i in range(len(payload)):
                    # print('I', i)
                    # print('PAILOAD I', payload[i])
                    payload_str = '{\"0\": \"'+payload[i]+'\"}'
                    # print('KEYS', keys['buttons'][i][0]['action']['payload'])
                    keys['buttons'][i][0]['action']['payload'] = payload_str
                    # print('NEW KEYS', keys['buttons'][i][0]['action']['payload'])
            else:
                for i in range(len(keys)):
                    # print('PAILOAD I2', payload[i])
                    payload_str = '{\"0\": \"'+payload[i]+'\"}'
                    keys['buttons'][i][0]['action']['payload'] = payload_str
        print('PAYLOAD UPDATED')
            







if __name__ == '__main__':
    key = Keyboards()
    print('*'*50)
    # key_list = ['😎 I’m good, like you my Queen', '🤓 Easy', '🤓 Always']
    # keyboard = key.create_keyboard_from_graph(key_list, ['hello', 'bay bay'])
    # pprint(keyboard)
    print('*'*50)
    key_list = ['🤓 Easy']
    #keyboard = key.create_keyboard_from_graph(key_list, ['hello', 'bay bay'])
    #pprint(keyboard)
    # print('*'*50)
    # key_list = []
    # keyboard = key.create_keyboard_from_graph(key_list, ['hello'])
    # pprint(keyboard)