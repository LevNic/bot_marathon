import os
import shutil
import requests
import re

from config_bot import name_marathon

class FileManager:

    def __init__(self):
        # Путь и файлы в рабочей директории бота
        self.name_marathon = name_marathon
        self.__create_marathon_directory()
        self.__path_data = f'CsvFile/{self.name_marathon}/'
        self.__path_sharing = f'GoogleDrive/{self.name_marathon}/'
        self.list_file_data = self.__lisf_file_clear(self.__path_data)
        self.list_file_sharing = self.__lisf_file_clear(self.__path_sharing)
        self.current_directory = os.getcwd()
        
    # Выбираем все скрытые файлы и удаляем их из списка файлов директории.
    # Возвращаем список только с файлами данных
    def __lisf_file_clear(self, path):
        list_f = os.listdir(path=path)
        pattern = re.compile(r'^\.\w+')
        for f in list_f[:]:
            if pattern.findall(f):
                list_f.remove(pattern.findall(f)[0])
        return list_f

    # Создаем директории для марафона, если их нет
    def __create_marathon_directory(self):
        list_data = os.listdir(path='CsvFile/')
        list_sharing = os.listdir(path='GoogleDrive/')
        print('NAME MARATHON', self.name_marathon)
        if self.name_marathon in list_data:
            print('DIRECTORY DATA YES')
        else:
            os.mkdir(f'CsvFile/{self.name_marathon}')
        if self.name_marathon in list_sharing:
            print('DIRECTORY SHARING YES')
        else:
            os.mkdir(f'GoogleDrive/{self.name_marathon}')
        
    '''
    Определяем есть ли в файлообменнике файлы, которых нет в данных.
    Если таких нет, то выясняем были ли файлы в файлообменнике обновлены.
    Возвращаем список файлов, которые следует добавить(изменить) в данные
    из файлообменника.
    '''
    def __directory_comparison(self):
        flag = False
        update_file = []
        for f in self.list_file_sharing:
            if f not in self.list_file_data:
                update_file.append(f)
                flag = True
                print('DIRECTORY', flag)
            elif f in self.list_file_data and os.path.getmtime(f'{self.__path_sharing}{f}') > os.path.getmtime(f'{self.__path_data}{f}'):
                flag = True
                update_file.append(f)
                print('FILE', flag)
        return update_file

    # Обновление файлов в GooglDrive директории текущего марафона
    def updata_file(self):
        path = os.path.join(self.current_directory, self.__path_sharing)
        print('PATH', path)
        return os.system(f'rclone sync google:Bot/{self.name_marathon}/ {path} -P')

    # Обновление файлов графа
    def update_graph(self):
        status = {}
        update_file = self.__directory_comparison()
        print('UPDATE FILE', update_file)
        if len(update_file) > 0:
            for f in update_file:
                path_sharing = os.path.join(self.__path_sharing, f)
                path_data = os.path.join(self.__path_data, f)
                result = shutil.copy(path_sharing, path_data)
                if result == path_data:
                    status[path_data] = 'Ok'
                else:
                    status[path_data] = 'No'
        return status

    # Проверка правильности названий файлов
    def __check_file_name(self):
        print('CHECKING FILE NAME')
        self.list_file_sharing = self.__lisf_file_clear(self.__path_sharing)
        for f in self.list_file_sharing:
            if re.findall(self.name_marathon, f) and not re.findall(' ', f) and re.findall(r'-.+_?.+\.csv', f):
                print('FILE NAME OK', f)
            else:
                print('BAD FILE NAME:', f)
                return f'BAD FILE NAME:, {f}'
        main_file = f'{self.name_marathon}-vertex.csv'
        if main_file not in self.list_file_sharing:
            print('NOT MAIN FILE')
            return('NOT MAIN FILE') 
        else:
            return 'OK'      
    
    # Создание списка структуры данных графа на основании файлов
    def create_graph_struct(self):
        graf_struct = []
        main_file = f'{self.name_marathon}-vertex.csv'
        self.list_file_data = self.__lisf_file_clear(self.__path_data)
        for name in self.list_file_data:
            if re.findall(main_file, name):
                graf_struct.append(name)
        if graf_struct[0]:
            for name in self.list_file_data:
                if not re.findall(main_file, name):
                    stage = re.split('-', name)
                    stage[0] = name
                    stage[1] = re.sub(r'.csv', r'', stage[1])
                    graf_struct.append(stage)
        else:
            print('STRUCTURE OF GRAF NOT CREATED')    
        print('СТРУКТУРА ГРАФА', graf_struct)
        return graf_struct

    def run_manager(self):
        self.updata_file()
        result_checking = self.__check_file_name()
        if result_checking == 'OK':
            print('RESULT', result_checking)
            if len(self.update_graph()) > 0:
                new_struct = self.create_graph_struct()
                print('MARTHAON SUCCESSFULLY CREATED')
                message = 'MARATHON SUCCESSFULLY CREATED'
                return new_struct
            else:
                new_struct = []
                message = 'NOT NEW FILE'
                print(message)
        else:
            print('MARATHON NOT CREATED')
            message = 'MARATHON NOT CREATED'
            new_struct = []
        return new_struct

