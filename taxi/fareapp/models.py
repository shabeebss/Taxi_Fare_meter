from django.db import models

# Create your models here.
class Login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class VehicleType(models.Model):
    type=models.CharField(max_length=100)
    price = models.IntegerField()
    seats=models.BigIntegerField()

class Driver(models.Model):
    LOGIN=models.ForeignKey(Login_table, on_delete=models.CASCADE)
    VTYPE=models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    vehnum=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    licencep=models.FileField()
    registrationp=models.FileField()
    insurancep=models.FileField()
    vehiclep=models.FileField()
    qr=models.FileField(null=True,blank=True)

class Customer(models.Model):
    LOGIN = models.ForeignKey(Login_table, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)

class Trip(models.Model):
    DRIVER=models.ForeignKey(Driver, on_delete=models.CASCADE)
    CUSTOMER=models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    splace=models.CharField(max_length=100)
    start=models.CharField(max_length=100)
    end=models.CharField(max_length=100)
    eplace=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField()
    distance=models.CharField(max_length=100)
    price=models.IntegerField(null=True,blank=True)
    bill = models.FileField(null=True,blank=True)
    payment = models.CharField(max_length=30,default='pending')

class Bill(models.Model):
    CUSTOMER=models.ForeignKey(Customer, on_delete=models.CASCADE)
    cost=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)


class Rating(models.Model):
    TRIP = models.ForeignKey(Trip, on_delete=models.CASCADE)
    rating=models.BigIntegerField()
    review=models.CharField(max_length=100)
    date=models.DateField()

