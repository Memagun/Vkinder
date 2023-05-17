import vk_api

from pprint import pprint
from config import access_token
from vk_api.exceptions import ApiError


class VkTools:
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)
        self.city_title = 0
        self.sex = 0
        self.age_from = 0
        self.age_to = 0
        self.user_id = 0

    def get_profile_info(self, user_id): #
        try:
            info = self.ext_api.method('users.get',
                                       {"user_id": user_id,
                                        "fields": "bdate, city, sex, relation"
                                       }
                                       )
            info_result = []
            info_result.append(*info)
        except ApiError:
            return

        return info_result

    def user_search(self, city_id, age_from, age_to, sex, offset=None): #
        try:
            profiles = self.ext_api.method('users.search',
                                       {"city_id": city_id,
                                        "age_from": age_from,
                                        "age_to": age_to,
                                        "sex": sex,
                                        "count": 10,
                                        "offset": offset,
                                        "fields": "city"
                                        })
        except ApiError:
            return

        profiles = profiles['items']
        result = []
        for profile in profiles:
            if not profile['is_closed']:
                self.city_title = profiles[0]["city"]["title"]
                result.append({"name": profile["first_name"] + " " + profile["last_name"],
                               "id": profile["id"],
                               "city_title": self.city_title
                               })
        return result

    def photos_get(self, user_id): #
        attachments = []
        photos = self.ext_api.method("photos.get",
                                     {"album_id": "profile",
                                      "owner_id": user_id,
                                      "extended": 1
                                     }
                                     )
        try:
            photos_i = photos["items"]
        except KeyError:
            return

        most_likes_photos = []
        for photo in photos_i:
            most_likes_photos.append({"owner_id": photo["owner_id"],
                                      "count": photo["likes"]["count"],
                                      "id": photo["id"]})
            most_likes_photos = sorted(most_likes_photos, key=lambda x: x["count"], reverse=True)
        for num, items in enumerate(most_likes_photos):
            most_likes_photos.append({"owner_id": items["owner_id"],
                                      "id": items["id"]})
            try:
                attachments.append("photo{}_{}".format(user_id, most_likes_photos[0]))
                attachments.append("photo{}_{}".format(user_id, most_likes_photos[1]))
                attachments.append("photo{}_{}".format(user_id, most_likes_photos[2]))
                return attachments
            except IndexError:
                print("Photos not found")

            if num == 2:
                break


bot = VkTools(access_token)

if __name__ == "__main__":
    # print(bot.user_search(1, 20, 40, 2))
    # print(bot.photos_get(1))
    bot.get_profile_info(bot.user_id)
    bot.user_search(bot.city_title, bot.sex, bot.age_from, bot.age_to)
    bot.photos_get(bot.user_id)


