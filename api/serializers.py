from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from api.models import Task

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=16,
        write_only=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super().create(validated_data)
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed')


class ExtendedTaskSerializer(TaskSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    updater = serializers.ReadOnlyField(source='updater.username', required=False)
