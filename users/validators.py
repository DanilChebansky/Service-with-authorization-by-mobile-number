from rest_framework.exceptions import ValidationError


def phone_validator(string):
    if string[0:2] != "79" or not string.isdigit() or len(string) != 11:
        raise ValidationError("Введите номер в формате 7900000000")
