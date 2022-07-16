import uuid

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from .models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

            pwd_valid = check_password(password, user.password)

            if not pwd_valid:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6, write_only=True, required=True)
    username = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        email = data.get("email")
        if email:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("That email is already in use")
        return data

    def create(self, validated_data):

        # Set the username server-side
        validated_data["username"] = uuid.uuid4()

        user = super(UserSerializer, self).create(validated_data)
        user.is_active = True

        # For creating users we must hash their password before storing
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        )
