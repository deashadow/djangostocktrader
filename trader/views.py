from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Product, BankAccount, Stock
from .forms import BankAccountForm, StockForm #ProductForm
import yfinance as yf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from django.conf import settings
import os
import urllib, base64
import io

#pk_ccf5633147854b7ea5f5a155f396da5a

# Create your views here.
def home( request):
    return render( request, 'home.html', {})


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

    if request.method == 'POST':
        bankaccount = request.POST['bankaccount']
        context = {'bankaccountForm' : BankAccountForm}
        return render ( request, 'product.html', {"bankaccountForm": BankAccountForm})

    else: 
        return render(request, 'product.html' , {})


def ticker_chart( request):
    import requests
    import json

    if request.method == 'POST':
        tchart = request.POST['tchart']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + tchart + "/chart/5d?token=pk_ccf5633147854b7ea5f5a155f396da5a")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'ticker_chart.html' , {'api': api } )

    else: 
        return render(request, 'ticker_chart.html' , {})


def add_stock(request):
    import requests 
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added to your Portfolio! "))
            return redirect('add_stock')
    else: 
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_3a23ad6ed1d84ad1b10f01c72dc2d07e")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html' , {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been deleted !"))
    return redirect('delete_stock')

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html' , {'ticker': ticker})



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

def products( request):
    print('products called')
    products = Product.objects.all();
    context = { 'products' : products}
    return render( request, 'products.html', context)

def bankaccount( request):
    bankaccountForm = BankAccountForm()
    return render( request, 'product.html', {"bankaccountForm": BankAccountForm})
    


def bankroll(request):
    bankroll = BankAccount.objects.all()
    context = {
        'user': user,
        'balance': balance,
    }
    return render(request, 'bankroll' , context)




def getPrice( request, id):
    ticker = yf.Ticker(id)
    retval = { "price" : ticker.info['regularMarketPrice']}
    return JsonResponse(retval)
    
def getInfo( tchart):
    import requests
    import json
    STARTDATE = '2014-01-01'
    ENDDATE = str( datetime.now().strftime('%Y-%m-%d'))
    company = yf.download( tchart, start=STARTDATE, end=ENDDATE)
    hist = company['Adj Close']
    hist.plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted")
    plt.title( tchart + " Price Data")
    plt.show()
    IMGDIR = os.path.join( settings.BASE_DIR, 'trader/static')
    print('IMGDIR', IMGDIR)
    plt.savefig( IMGDIR + '/my_plot.png')
    plt.savefig( './trader/static/my_plot.png')



def getTotal( request):
    id = int(request.POST.get['id'])
    print('getTotal:id='+str(id))
    bankaccount = get_object_or_404( BankAccount, id=id)
    total = bankaccount.getTotalCost()
    return JsonResponse( {'total': total})