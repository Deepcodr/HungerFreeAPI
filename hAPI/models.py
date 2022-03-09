from django.db import models

# Create your models here.

class Request(models.Model):
    Name = models.CharField(max_length=100)
    UserID = models.CharField(max_length=50)
    Email=models.CharField(max_length=100)
    Place_id = models.CharField(max_length=200)
    Lat=models.DecimalField(null=True,max_digits=12,decimal_places=10)
    Lng=models.DecimalField(null=True,max_digits=18,decimal_places=15)

class donation(models.Model):
    Name = models.CharField(max_length=100)
    UserID = models.CharField(max_length=50)
    Email=models.CharField(max_length=100)
    Place_id = models.CharField(max_length=200)
    Lat=models.DecimalField(max_digits=12,decimal_places=10,null=True)
    Lng=models.DecimalField(max_digits=18,decimal_places=15,null=True)

class UserData(models.Model):
    Type=models.CharField(max_length=2)
    create_name=models.CharField(max_length=100)
    create_uid=models.CharField(max_length=50)
    accept_uid=models.CharField(max_length=50)
    # accept_email=models.CharField(max_length=100)
    Lat=models.DecimalField(max_digits=12,decimal_places=10,null=True)
    Lng=models.DecimalField(max_digits=18,decimal_places=15,null=True)