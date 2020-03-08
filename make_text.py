# Создание текста сообщений
 
import random
import re



# Класс сообщения
class TextPreparation:
    # Имя пользователя
    name = 'Uno'
    # Словарь для записи параметров сообщения
    message = {}
    
    def __init__(self, name):
        self.name = name
        self.pattern_name = re.compile(r'NAME')

    def send_name(self, message):
        return re.sub(self.pattern_name, self.name, message)
    
    def clear_text(self, text):
        pattern = re.compile(r'\w+')
        this_text = re.findall(pattern, text)
        for n in range(len(this_text)):
            this_text[n] = this_text[n].lower()
            print('This text', this_text)
        return this_text   




if __name__ == '__main__':
    message = 'NAME, привет. Это бот.'
    text = TextPreparation('Ivan')
    print(text.send_name(message))