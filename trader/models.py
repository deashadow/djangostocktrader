from django.db import models
from django.contrib.auth.models import User

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