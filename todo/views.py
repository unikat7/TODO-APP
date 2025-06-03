from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response 
from rest_framework import status,permissions
from django.contrib.auth.models import User
from .models import ToDo
from .serializers import UserSerializer,ToDoSeriailizer
from rest_framework.views import APIView

class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"User registered successfully"
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class ToDoListCreate(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        todos=ToDo.objects.filter(user=request.user)
        serializer=ToDoSeriailizer(todos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer=ToDoSeriailizer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ToDoDetail(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self,pk,user):
        return get_object_or_404(ToDo,pk=pk,user=user)
    
    def get(self,request,pk):
        todo=self.get_object(pk,request.user)
        serializer=ToDoSeriailizer(todo)
        return Response(serializer.data)
    
    def put(self,request,pk):
        todo=self.get_object(pk,request.user)
        serializer=ToDoSeriailizer(todo,data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)###Ensure it doesnot change the current user
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        todo=self.get_object(pk,request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









