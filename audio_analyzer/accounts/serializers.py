import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

SIGNUP_ERROR_MESSAGE = (
    "Both password and username must contain at least 8 characters, "
    "and the password must contain at least "
    "one uppercase letter and one special character")

NOT_FOUND_MESSAGE = "No such user, or incorrect credentials provided"

EXISTING_USER_MESSAGE = "Such user already exists"

UserCustomModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustomModel
        fields = '__all__'

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        if not (self.regex_password_validator(password) and len(username) > 8):
            raise serializers.ValidationError(SIGNUP_ERROR_MESSAGE)
        return attrs

    def create(self, validated_data):
        created_user = UserCustomModel.objects.create(**validated_data)
        created_user.set_password(validated_data.get('password', None))
        created_user.save()
        return created_user

    @staticmethod
    def regex_password_validator(password):
        pattern = r'^(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return bool(re.match(pattern, password))
