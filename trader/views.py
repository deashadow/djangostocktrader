from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import BankAccount, Stock, StockProduct
from .forms import BankAccountForm, StockForm, StockProductForm
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
import urllib, base64, requests
import io
import json as simplejson
#import seaborn as sns 
from django.conf import settings
#from matplotlib import rcParams

#pk_ccf5633147854b7ea5f5a155f396da5a

# Create your views here.
def home( request):
    print('home')
    print(request)
    return render( request, 'home.html')


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


def stockproduct( request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Purchase Has Been Added to your Portfolio! "))
            return redirect('trading')
    stockproductForm = StockProductForm()
    context = { 'stockproductForm' : stockproductForm}
    return render( request, 'trading.html', context)

# def getTotalCost( self):  #buy function
#         return float(self.current_price * self.quantity)



def ticker_chart( request):
    import requests
    import json

    if request.method == 'POST':
        tchart = request.POST['tchart']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + tchart + "/chart/7d?token=pk_ccf5633147854b7ea5f5a155f396da5a")
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
        print(username)
        user = authenticate( request, username=username, password=password)
        if user is not None:
            print('ron')
            login( request, user)
            messages.success( request, ('You have been Successfully logged in!!'))
            print(request)
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

def trading( request):
    return render( request, 'trading.html', {})

def contact( request):
    return render( request, 'contact.html', {})

""" def products( request):
    print('products called')
    products = Product.objects.all();
    context = { 'products' : products}
    return render( request, 'products.html', context) """

def bankaccount( request):
    bankaccountForm = BankAccountForm()
    return render( request, 'trading.html', {"bankaccountForm": BankAccountForm})
    


def bankroll(request):
    bankroll = BankAccount.objects.all()
    context = {
        'user': user_id,
        'bank_balance': bank_balance_id,
    }
    return render(request, 'bankroll' , context)




def getPrice( request, id):
    print('getPrice id='+str(id))
    ticker = yf.Ticker(id)
    print('ticker='+str(ticker))
    retval = { "price" : ticker.info['regularMarketPrice']}
    print('retval='+str(retval))

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



def getTotalCost( request):
    print('getTotalCost')
    symbol = request.POST['symbol']
    print('getTotalCost:symbol='+symbol)
    stockproduct = get_object_or_404( StockProduct, name=symbol)
    total = stockproduct.getTotalCost()
    print('getTotalCost:total='+str(total))
    return JsonResponse( {'total': total})





def my_stock_plot_view( request, number):
    # get stock data
    json_data = simplejson.dumps(data)
    return render(request, 'ticker_chart.html', {'json_plot_data': json_data})





""" RAPIDAPI_KEY  = "8b6377d157msh2440774f3177ecbp1830a4jsn082485ce7a25" 
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"

symbol_string = ""
inputdata = {}

def fetchStockData(symbol):
  
  response = requests.request("https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?region=US&lang=en&symbol=" + symbol + "&interval=1d&range=3mo",
    headers={
      "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com",
      "X-RapidAPI-Key": "8b6377d157msh2440774f3177ecbp1830a4jsn082485ce7a25",
      "Content-Type": "application/json"
    }
  )
  
  if(response.code == 200):
    return response.body
  else:
    return None


def parseTimestamp(inputdata):

  timestamplist = []

  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])

  calendertime = []

  for ts in timestamplist:
    dt = datetime.fromtimestamp(ts)
    calendertime.append(dt.strftime("%m/%d/%Y"))

  return calendertime

def parseValues(inputdata):

  valueList = []
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])

  return valueList


def attachEvents(inputdata):

  eventlist = []

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("open")  

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("close")

  return eventlist


if __name__ == "__main__":

  try:

    while len(symbol_string) <= 2:
      symbol_string = raw_input("Enter the stock symbol: ")

    retdata = fetchStockData(symbol_string)

    

    if (None != inputdata): 

      inputdata["Timestamp"] = parseTimestamp(retdata)

      inputdata["Values"] = parseValues(retdata)

      inputdata["Events"] = attachEvents(retdata)

      df = pd.DataFrame(inputdata)

      sns.set(style="darkgrid")

      rcParams['figure.figsize'] = 13,5
      rcParams['figure.subplot.bottom'] = 0.2

      
      ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",dashes=False, markers=True, 
                   data=df, sort=False)


      ax.set_title('Symbol: ' + symbol_string)
      
      plt.xticks(
          rotation=45, 
          horizontalalignment='right',
          fontweight='light',
          fontsize='xx-small'  
      )

      plt.show()

  except Exception as e:
    print ("Error" )  
    print (e) """