from rest_framework import serilaizers
from django.contrib.auth.models import User



class UserSerializer(serilaizers.ModelSerilaizer):
    confirm_password=serilaizers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','password']
        extra_kwargs={
            'password':{
                'write_only':True
            }
        }
        def validate(self,data):
            if data['password']!=data['confirm_password']:
                raise serilaizers.ValidationError("password doesnot match")
            return data



        def create(self,validated_data):
            validated_data.pop('confirm_password')
            return User.objects.create(**validated_data)


class ToDoSeriailizer(serilaizers.ModelSerilaizer):
    class Meta:
        models=ToDo
        fields='__all__'
