import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import threading

_vk = None

def start(token):
    global _vk
    _vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(_vk)
    print("VK бот запущен...")
    
    def listen():
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                # Базовая эхо-логика
                _vk.method('messages.send', {'user_id': event.user_id, 'message': 'Я получил твое сообщение!', 'random_id': 0})
                
    threading.Thread(target=listen, daemon=True).start()

запустить = start