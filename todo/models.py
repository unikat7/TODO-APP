from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Test(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

