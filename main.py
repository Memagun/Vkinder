import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import engine
from engine import *
from config import access_token, community_token



class BotInterface:

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)

    def message_send(self, user_id, message, attachment=None):
        self.bot.method("messages.send",
                        {
                            "user_id": user_id,
                            "message": message,
                            "random_id": get_random_id(),
                            "attachment": attachment
                        }
                        )

    def handler(self):
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                user_request = event.text.lower()
                if user_request == "привет":
                    self.message_send(event.user_id,
                                      "Приветствую, я бот Vkinder\n"
                                      "Я осуществляю поиск подходящей по критериям пары\n"
                                      "Критерии: город, возраст в промежутке от -4 лет до +4 лет\n"
                                      "Для старта введите команду 'поиск'\n"
                                      "Для окончания работы со мной введите 'пока'\n"
                                      "Для продолжения работы напишите 'далее'\n")
                elif user_request == "поиск":
                    self.message_send(event.user_id, "начинаю поиск")
                    matched_users_list = []
                    bot.get_profile_info(user_id)
                    users_search = bot.user_search(bot.city_title, bot.sex, bot.age_from, bot.age_to)
                    for profile in users_search:
                        id = profile["id"]
                        matched_users_list.append(id)
                    ids_f = matched_users_list.pop()
                    founded_user = str("vk.com/id" + str(ids_f))
                    attachment = bot.photos_get(ids_f)
                    self.message_send(user_id, founded_user, attachment=attachment)
                    self.message_send(user_id, "Для продолженния введите 'далее'")
                elif user_request == "далее":
                    pass
                elif user_request == "пока":
                    break
                else:
                    self.message_send(event.user_id, "неизвестная команда")


if __name__ == "__main__":
    bots = BotInterface(community_token)
    bots.handler()
    # media = f"photo_ownerid_photoid"
    # bot.message_send(id, "Фото", attachment=media)

