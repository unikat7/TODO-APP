from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response 
from rest_framework import status,permissions
from djanngo.contrib.auth.models import User
from .models import ToDo
from .serilaizers import UserSerializer,ToDoSeriailizer
from rest_framework.views import APIView

class RegsiterView(ApiView):
    def post(self,request):
        serilaizer=UserSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response({
                "message":"User registered successfully"
            },status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class ToDoListCreate(APIView)

