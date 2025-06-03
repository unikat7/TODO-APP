
from django.urls import path
from .views import RegisterView, ToDoListCreate, ToDoDetail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('todos/', ToDoListCreate.as_view(), name='todos'),
    path('todos/<int:pk>/', ToDoDetail.as_view(), name='todo-detail'),
]
