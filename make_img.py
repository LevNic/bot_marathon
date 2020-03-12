# Создание картинок
import requests

from vk_metod import VkMethod

class ImagesFile:

    method = VkMethod()

    def make_img_file(self, image_url):    
        file_name = image_url.split('/')[-1]
        file_path = f'Images/{file_name}'
        r = requests.get(image_url)
        if r.status_code == 200:
            print('Success img resource!')
            with open(file_path, 'wb') as f:
                f.write(r.content)
            return file_path
        else:
            print('Not images')

    def attachment_for_graph(self, name_file):
        print('FILE NAME FOR ATTACHMENT', name_file)
        photo = self.method.upload().photo_messages(photos=name_file)[0]
        # print('PHOTO', photo)
        owner_id = photo['owner_id']
        photo = photo['id']
        attach = f'photo{owner_id}_{photo}'
        return attach


    def attachment_series(self, file_img):
        if file_img:
            photo = self.method.upload().photo_messages(photos=file_img)[0]
            owner_id = photo['owner_id']
            photo = photo['id']
            attach = f'photo{owner_id}_{photo}'
        else:
            attach = 0
        return attach

if __name__ == '__main__':
    img = ImagesFile()
    path = img.make_img_file('https://cp.beget.com/i/logo@x2.png')
    print('PAHT', path)
