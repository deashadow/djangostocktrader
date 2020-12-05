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
    


class Share(models.Model):
    ticker = models.CharField(max_length=10)
    def __str__(self):
      return self.ticker
    """ def getShareValue( self):
        return float(self.stockprice * self.quantity) """

class Quote( models.Model):
    stock_name = models.CharField( max_length=30)
    price = models.DecimalField( max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"name={self.stock_name}, price={self.price}, quantity={self.quantity}"


class Account(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    balance=models.FloatField(default=100000)
    created=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} [${self.balance}]"
 
class Stock(models.Model):
    symbol=models.CharField(max_length=8)
    company_name=models.CharField(max_length=512)
    quantity=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    account=models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.symbol} {self.company_name} @ {self.quantity} "
 



#class Category(models.Model):
 # icon = Iconfield