from calendar import monthrange
from datetime import datetime
from datetime import time as tm
from dateutil import rrule
from time import sleep, ctime, time
import threading




class SetTimes:

    def __init__(self, id_timer):
        self.minute = datetime.now().minute
        self.hour = datetime.now().hour
        self.day = datetime.now().day
        self.month = datetime.now().month
        self.year = datetime.now().year
        self.id_timer = id_timer
        self.number_of_post = 4

    # Текущее время в зоне работы программы
    def time_now(self):
        return datetime.now()

    # Текущее время в UTC
    def time_now_utc(self):
        return datetime.utcnow()

    # Количество дней до конца месяца
    def end_of_month(self):
        return monthrange(datetime.now().year, datetime.now().month)[1] - datetime.now().day
    
    # Список параметров цикла ежедневных сообщений
    def message_loop(self):
        list_rrule = list(rrule.rrule(rrule.DAILY, count=self.number_of_post, dtstart=datetime.now()))
        for item in list_rrule:
            delta = item - datetime.now()
            second = delta.total_seconds()
            if second <= 0:
                print('The selected data is less than the current data')
                flag = False
            else:
                sleep(second)
                print('Flag is True')
                flag = True
                # get_message = 'Проверка'
                #self.post.post_all(get_message)
            return flag

    def slipping(self, number_of_post):
        list_rrule = list(rrule.rrule(rrule.MINUTELY, count=number_of_post, dtstart=datetime.now()))
        for item in list_rrule:
            delta = item - datetime.now()
            second = delta.total_seconds()
            if second > 0:
                print('return sleep')
                return sleep(second)
                

    def get_of_time(self):
        list_rrule = list(rrule.rrule(rrule.DAILY, count=self.number_of_post, dtstart=datetime.now()))
        for item in list_rrule:
            if item == datetime.now():
                get_message = 'Проверка'
                print(get_message)
                return get_message


    # Установка минут пользователем
    def setting_minutes_user(self, minute):
        try:
            minute = int(minute)
        except ValueError:
            message = 'Минуты введены не корректно. Введите число от 0 до 59'
        else:
            if minute > 59 or minute < 0:
                message = f'{minute} - неверное значение. Введите значение от 0 до 59.'
            else:
                self.minute = minute
                message = f'Установлено {self.minute} минут'
        
        return message

    # Установка часов пользователем
    def setting_hours_user(self, hours):
        try:
            hours = int(hours)
        except ValueError:
            message = 'Часы введены не корректно. Введите число от 0 до 23'
        else:
            if hours > 23 or hours < 0:
                message = f'{hours} - неверное значение. Введите значение от 0 до 23.'
            else:
                self.hour = hours
                message = f'Установлено {self.hour} часов'
        
        return message

    # Установка даты пользователем
    def setting_date_user(self, date):
        try:
            date = int(date)
        except ValueError:
            message = 'Дата введена не корректно. Введите дату от 0 до ...'
        else:
            if date > 23 or date < 0:
                message = f'{date} - неверное значение. Введите значение от 0 до ....'
            else:
                self.date = date
                message = f'Установлено {self.date} число'
        
        return message


    # Установка минут ботом
    def setting_minutes(self, minute):
        self.minute = minute

    # Установка часов ботом
    def setting_hour(self, hour):
        self.hour = hour
    
    # Установка даты ботом
    def setting_date(self):
        pass

    # Возвращает True в заданное время
    # y - год;
    # month - месяц;
    # d - день;
    # h - час;
    # minut - минута;
    def timer(self, y, month, d, h, minut):
        try:
            datetime(y, month, d, h, minut)
        except ValueError:
            print('The data is not correct')
            flag = False
        else:
            delta = datetime(y, month, d, h, minut) - datetime.now()
            second = delta.total_seconds()
            if second <= 0:
                print('The selected data is less than the current data')
                flag = False
            else:
                sleep(second)
                flag = True
        return flag
