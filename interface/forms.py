from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm, Form, CharField, forms

from users.models import User


class UserRegisterForm(ModelForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ("phone",)


class SmsCodeForm(Form):
    """Форма ввода кода"""

    code = CharField(label="Код из SMS")


class UserUpdateForm(UserChangeForm):
    """Форма обновления данных пользователя"""

    def clean_invite_input(self):
        """Проверяем invite_input"""
        invite_input = self.cleaned_data.get("invite_input")
        if self.instance.invite_input:
            raise forms.ValidationError("Вы уже использовали код")
        if not invite_input:
            return invite_input
        if invite_input == self.instance.invite_code:
            raise forms.ValidationError("Вы не можете использовать свой же код!")
        if not User.objects.filter(invite_code=invite_input).exists():
            raise forms.ValidationError("Пригласительный код не найден!")
        return invite_input

    class Meta:
        model = User
        fields = (
            "phone",
            "email",
            "city",
            "invite_input",
        )
