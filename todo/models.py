from django.db import models
from django.contrib.auth.models import User


class TODOO(models.Model):
    srno = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)   
    date = models.DateTimeField(auto_now_add=True)  
    status = models.BooleanField(default=False)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  




