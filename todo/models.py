from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDo(mdoels.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return self.title

        