from rest_framework.exceptions import ValidationError


class PhoneValidator:

    def __init__(self, phone):

        self.phone = phone

    def __call__(self, value):

        tmp_val2 = dict(value).get(self.phone)
        if tmp_val2[0:2] != "79" or not tmp_val2.isdigit() or len(tmp_val2) != 11:
            raise ValidationError("Введите номер в формате 79000000000")


def phone_validator(string):
    if string[0:2] != "79" or not string.isdigit() or len(string) != 11:
        raise ValidationError("Введите номер в формате 79000000000")
