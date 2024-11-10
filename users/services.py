import random

from users.models import User


def create_invite_code():
    str_list = []
    for i in range(97, 123):
        str_list.append(chr(i))
    for i in range(65, 91):
        str_list.append(chr(i))
    for i in range(1, 10):
        str_list.append(str(i))
    while True:
        invite_code = ""
        for i in range(6):
            invite_code += str_list[random.randint(0, len(str_list) - 1)]
        if (
            any(i.isupper() for i in invite_code) and any(i.islower() for i in invite_code) and sum(i.isdigit() for i in invite_code) >= 3 and invite_code not in [user.invite_code for user in User.objects.all()]
        ):
            break
    return invite_code
