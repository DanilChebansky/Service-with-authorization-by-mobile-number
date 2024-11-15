from rest_framework.exceptions import ValidationError
from users.models import User


class InviteInputValidator:

    def __init__(self, invite_input, phone):
        self.invite_input = invite_input
        self.users = User.objects.all()
        self.phone = phone

    def __call__(self, value):
        tmp_val1 = dict(value).get(self.invite_input)
        tmp_val2 = dict(value).get(self.phone)
        user = self.users.filter(phone=tmp_val2).first()
        if user.invite_input:
            if tmp_val1:
                raise ValidationError("Пригласительный код уже был введен")
        else:
            if tmp_val1:
                if user.invite_code == tmp_val1:
                    raise ValidationError("Нельзя вводить свой же пригласительный код")
                elif not self.users.filter(invite_code=tmp_val1).exists():
                    raise ValidationError("Пригласительный код не найден!")
