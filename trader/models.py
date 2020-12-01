from django.db import models
from django.contrib.auth.models import User
import datetime
#from fontawesome_5.fields import Iconfield
# Create your models here.


class StockProduct( models.Model):
    name = models.CharField( max_length=30)
    price = models.DecimalField( max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    def __str__( self):
        return "{}, name={}, price={}, quantity={}".format( self.id, self.name, self.price, self.quantity)
    def getTotalCost( self):  #buy function
         return float(self.price * self.quantity) 


class BankAccount( models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bank_balance=models.FloatField(default=2500)
    created=models.DateTimeField( auto_now_add=True)
    last_modified=models.DateTimeField( auto_now=True)
    def __str__( self):
      return "user={}, bank_balance={}".format( self.user, self.bank_balance)
    


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    def __str__(self):
      return self.ticker
    def getShareValue( self):
      return float(self.stockprice * self.quantity)


#class Category(models.Model):
 # icon = Iconfield