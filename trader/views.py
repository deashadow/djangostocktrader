from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Product, BankAccount
from .forms import BankAccountForm #ProductForm
import yfinance as yf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages

#pk_ccf5633147854b7ea5f5a155f396da5a

# Create your views here.
def home( request):
    return render( request, 'home.html', {})

#def product( request):
 #   return render( request, 'product.html', {})

def product( request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_ccf5633147854b7ea5f5a155f396da5a")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'product.html' , {'api': api })

    else: 
        return render(request, 'product.html' , {})
    return render( request, 'product.html', {})


def login_user( request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate( request, username=username, password=password)
        if user is not None:
            login( request, user)
            messages.success( request, ('You have been Successfully logged in!! Let us start Tradding'))
            return redirect('home')
           # return render( request, 'home.html')
        else:
            messages.success( request, ('Error logging in??  Please try again...'))
            return redirect('login')
    else:
        return render ( request, 'login.html', {})
    


def logout_user( request):
    #logout(request)
    #messages.success( request, ('You have successfully logged out---See you soon!!'))
    return render(request, 'registration/logout.html')

#def registration( request):
   # return render( request, 'registration_form.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def about( request):
    return render( request, 'about.html', {})

def contact( request):
    return render( request, 'contact.html', {})

#def products( request):
  #  print('products called')
   # products = Product.objects.all();
   # context = { 'products' : products}
    #return render( request, 'products.html', context)

#def product( request):
 #   print('product 1')
 #   if request.method == 'POST':
 #       productForm = ProductForm( request.POST)
 #       if productForm.is_valid() == False:
 #           return HttpResponse( productForm.errors)
 #       productForm.save();
 #       return redirect("/product");
 #   elif request.method == 'GET':
 #       productForm = ProductForm()
 #   print('product 2')
 #   context = { 'productForm' : productForm}
   # productForm.save();
 #   return render( request, 'product.html', context)


def account(request):
    balance = balance.objects.all()
    #count = balance.objects.all().count()
    context = { 
        #'count': count,
        'balance': balance,
    }
   # productForm.save();
    return render( request, 'home.html', context)




def getPrice( request, id):
    ticker = yf.Ticker(id)
    retval = { "price" : ticker.info['regularMarketPrice']}
    return JsonResponse(retval)
    


