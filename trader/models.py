from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
#class Product( models.Model):
 #   name = models.CharField( max_length=30)
  #  price = models.DecimalField( max_digits=8, decimal_places=2)
  #  quantity = models.IntegerField()



class Product( models.Model):
    name = models.CharField( max_length=30)
    price = models.DecimalField( max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    def __str__( self):
        return "name={}, price={}, quantity={}".format( self.name, self.price, self.quantity)


class BankAccount( models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    balance=models.FloatField(default=2500)
    created=models.DateTimeField( auto_now_add=True)
    last_modified=models.DateTimeField( auto_now=True)
    def __str__( self):
      return "user={}, balance={}".format( self.user, self.balance)
      


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    def __str__(self):
     return self.ticker