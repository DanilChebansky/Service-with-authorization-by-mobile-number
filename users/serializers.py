from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "email",
            "city",
            "invite_code",
            "invite_input",
        )


class ProfileSerializer(ModelSerializer):

    invitation_list = SerializerMethodField()

    def get_invitation_list(self, obj):
        users = User.objects.filter(invite_input=obj.invite_code)
        return [user.phone for user in users]

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
