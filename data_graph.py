# Класс для создания графа действий бота
import csv
import re

from file_manager import FileManager
from config_bot import name_marathon
from make_img import ImagesFile

file_manager = FileManager()
img = ImagesFile()
# Структура данных графа: [основной файл графа, [файл с веткой графа - вершина графа к которой прицеплена ветка], [...], [...]]
# data_for_graph = ['english_marathon-vertex.csv', ['english_marathon-hello.csv', 'hello'], 
#                ['english_marathon-small_steps.csv', 'small_steps' ]]
data_for_graph = file_manager.create_graph_struct()


def graph_creator(data_for_graph):

    graph = Graph(data_for_graph[0])
    if len(data_for_graph) >= 2:
        print('STEPS', len(data_for_graph))
        for i in range(1, len(data_for_graph)):
            print('I0', data_for_graph[i][0])
            graph.create_new_branch(data_for_graph[i][0], data_for_graph[i][1])
            print(f'STEP {i}: {data_for_graph[i][0]}, {data_for_graph[i][1]}')
    return graph


class Graph:

    pattern_key = re.compile(r'text_key_\d+_?\d*')
    pattern_type_key = re.compile(r'type_key_\d+_?\d*')

    def __init__(self, name_file):

        # CSV файл из которого берется информация для построения графа
        self.name_file = name_file
        self.name_marathon = name_marathon
        # Словарь типа vertexes = {vertex_1: [val_1, val_2 ...], vertex_2: []....}
        self.vertexes = {}
        self.__vertex_creation()
        # Словарь типа edges = {vertex_1: [vertex, ... вершины в которые есть путь],
        #                       vertex_2: vertex, ... вершины в которые есть путь],
        #                        и так далее ...}
        self.edges = {}
        self.__edges_from_vertices()
        
    # Получение данных из файла csv
    def csv_reader(self):
        data = []
        # print('NAME MARATHON', self.name_marathon)
        link_file = f'CsvFile/{self.name_marathon}/{self.name_file}'
        print('LINK', link_file)
        with open(link_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    # Создание вершин графа на основании файла
    def __vertex_creation(self):
        data = self.csv_reader()
        n = 0
        for d in data:
            # Создаем названия вершин, если их нет
            keys = self.vertexes.keys()
            while f'step_{n}' in keys:
                n += 1
            new_step_name = f'step_{n}'
            if d.get('step_name') == '':
                d['step_name'] = new_step_name
            key = d.pop('step_name')

            # Создаем текст, если его нет
            if d.get('text') == '':
                d['text'] = 'Простите, не помню этот текст. Поэтому пройдите на следующий этап.'
            
            # Удаляем ключи без данных
            empty_keys = []
            for k, v in d.items():
                if v == '':
                    empty_keys.append(k)
            for empty_key in empty_keys:
                del d[empty_key]

            # Создаем файл с картинкой, если картинка ссылка
            name_img = d.get('img')
            print('NAME IMG', name_img, type(name_img))
            
            if name_img:
                pattern = re.findall(r'^http.+', name_img)
                if len(pattern) > 0:
                    if name_img == pattern[0]:
                        like_img = img.make_img_file(d.get('img'))
                        d['img'] = like_img
                        print('LINK UPDATED', like_img)

            # Меняем тип данных text
            text_list = []
            text_list.append(d['text'])
            d['text'] = text_list
            self.vertexes[key] = d

            

    # Создание ребер из вершин
    def __edges_from_vertices(self):
        keys = list(self.vertexes.keys())
        for i in range(len(keys) - 1):
            # меняем тип данных на список
            edges_list = []
            edges_list.append(keys[i + 1])
            self.edges[keys[i]] = edges_list
        self.edges[keys[-1]] = 0


    # Создание новой ветки графа
    def create_new_branch(self, name_file, name_vertex):
        graph = Graph(name_file)    
        self.edges[name_vertex].append(list(graph.edges.keys())[0])  
        self.edges.update(graph.edges)
        self.vertexes.update(graph.vertexes)   

    # Ообновляет данные, добавляя новые вершины и их ребра.
    def data_updating(self, vertex, edge):
        self.vertexes.update([vertex])
        self.edges.update([edge])

# Список этапов серии
# series_list = ['small_steps', 'why', 'third_day', 'fourth_day', 'fifth_day', 'sixth_day', 'seventh_day', 'eighth_day',
#                     'ninth_day', 'tenth_day', 'eleventh_day', 'twelfth_day', 'thirteenth_day', 'fourteenth_day', 'fifteenth_day',
#                     'sixteenth_day']
def series_list_creator():
    graph = Graph(data_for_graph[0])
    series_list = list(graph.vertexes.keys())
    series_list.remove('hello')
    return series_list

series_list = series_list_creator()
