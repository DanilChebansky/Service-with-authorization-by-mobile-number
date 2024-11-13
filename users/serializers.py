from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import User
from users.serializer_validators import InviteInputValidator
from users.validators import PhoneValidator


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
        )

        validators = [PhoneValidator(phone="phone")]


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "city",
            "invite_input",
            "phone",
        )

        validators = [InviteInputValidator(invite_input="invite_input", phone="phone")]


class UserConfirmSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "sms",
        )


class ProfileSerializer(ModelSerializer):

    user_field_pk = SerializerMethodField()
    invitation_list = SerializerMethodField()

    def get_invitation_list(self, obj):
        users = User.objects.filter(invite_input=obj.invite_code)
        return [{"id": user.pk, "phone": user.phone} for user in users]

    def get_user_field_pk(self, obj):
        return obj.pk

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "email",
            "city",
            "invite_code",
            "invite_input",
            "invitation_list",
            "user_field_pk",
        )
