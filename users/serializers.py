from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import User
from users.serializer_validators import InviteInputValidator


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
        )


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            'phone',
            "email",
            "city",
            "invite_input",
        )

        validators = [InviteInputValidator(invite_input="invite_input", pk="id", phone="phone")]


class UserConfirmSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "sms",
        )


class ProfileSerializer(ModelSerializer):

    invitation_list = SerializerMethodField()

    def get_invitation_list(self, obj):
        users = User.objects.filter(invite_input=obj.invite_code)
        return [{"id": user.pk, "phone": user.phone} for user in users]

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
        )
