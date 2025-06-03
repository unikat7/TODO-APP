from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ToDo

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords donotttt match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class ToDoSeriailizer(serializers.ModelSerializer):
    class Meta:
       model=ToDo
       fields = ['id', 'title', 'completed'] 



