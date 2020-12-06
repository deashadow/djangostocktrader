from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import BankAccount, Stock, Share, Account, StockProduct
from .forms import BankAccountForm, ShareForm, StockProductForm
import yfinance as yf
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from datetime import datetime
from django.conf import settings
import pandas as pd
import numpy as np
import os
import urllib, base64, requests
import io
import json as simplejson
from matplotlib import pylab
import matplotlib.pyplot as plt

#from django.views.decorators.csrf import csrf_exempt
#import seaborn as sns 
#pk_ccf5633147854b7ea5f5a155f396da5a

# Create your views here.
def home( request):
    """ print('home')
    print(request)
    return render( request, 'home.html') """
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        stocks = Stock.objects.filter(account=account).order_by('-created').all()[:5]
        stock_symbols = stocks.values_list('symbol', 'quantity')
        account_value = sum([yf.Ticker(stock[0]).info["ask"]*stock[1] for stock in stock_symbols])
        account_value += account.balance
    else:
        account = None
        stocks = []
        account_value = 0
        
    context = {
        'account': account,
        'stocks': stocks,
        'stock_count': len(stocks) if stocks else 0,
        'account_value': account_value,
    }
        
    return render( request, 'home.html', context)



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
        form = StockProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Purchase Has Been Added to your Portfolio! "))
            return redirect('trading')
    stockproductForm = StockProductForm()
    context = { 'stockproductForm' : stockproductForm}
    return render( request, 'trading.html', context)



def ticker_chart( request):
    import requests
    import json

    if request.method == 'POST':
        tchart = request.POST['tchart']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + tchart + "/chart/7d?token=pk_ccf5633147854b7ea5f5a155f396da5a")
        try:
            api = json.loads(api_request.content)
            print(json.dumps(api, indent=4))
            date_range = [item ['date'] for item in api]
            close_value = [item ['uClose'] for item in api]
            open_value = [item ['uOpen'] for item in api]
            plt.plot(date_range, open_value)
            plt.plot(date_range, close_value)
            fig = plt.gcf()
            plt.close()
            #convert graph into string buffer and then convert 64bit code into actual image
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
        except Exception as e:
            api = "Error..."
        return render(request, 'ticker_chart.html' , {'data':uri,'api': api } )

    else: 
        return render(request, 'ticker_chart.html' , {'tchart':"Enter a Ticker Symbol in the search"})






def add_stock(request):
    import requests 
    import json

    if request.method == 'POST':
        form = ShareForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added to your Portfolio! "))
            return redirect('add_stock')
    else: 
        ticker = Share.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_3a23ad6ed1d84ad1b10f01c72dc2d07e")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html' , {'ticker': ticker, 'output': output})


def delete(request, share_id):
    item = Share.objects.get(pk=share_id)
    item.delete()
    messages.success(request, ("Stock Has Been deleted !"))
    return redirect('delete_stock')

def delete_stock(request):
    ticker = Share.objects.all()
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
    


""" def bankroll(request):
    bankroll = BankAccount.objects.all()
    context = {
        'user': user_id,
        'bank_balance': bank_balance_id,
    }
    return render(request, 'bankroll' , context) """




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


def getStockInfo( request, symbol):
    return JsonResponse({"symbol": symbol })



def getTotalCost( request):
    print('getTotalCost')
    symbol = request.POST['symbol']
    print('getTotalCost:symbol='+symbol)
    stockproduct = get_object_or_404( StockProduct, name=symbol)
    total = stockproduct.getTotalCost()
    print('getTotalCost:total='+str(total))
    return JsonResponse( {'total': total})

def get_stock_graph(symbol):
    STARTDATE = '2020-01-01'
    ENDDATE = str( datetime.now().strftime('%Y-%m-%d'))
    company = yf.download( symbol, start=STARTDATE, end=ENDDATE)
    hist = company['Adj Close']
    hist.plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted")
    plt.title( symbol + " Price Data")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def get_stock_info(stocks):
    ret = []
    for stock in stocks:
        stock_quote = yf.Ticker(stock.symbol).info
        sell_price = stock_quote["bid"]
        ret.append({"symbol": stock.symbol, "company_name": stock.company_name, "quantity": stock.quantity, "value": sell_price * stock.quantity})
    return ret

#@login_required
#@csrf_exempt

def trade(request):
    account = None
    stocks = []
    message = ""
    if request.user.is_authenticated:
        print('trade:authenticated')
        account = Account.objects.get(user=request.user)
        all_stocks = Stock.objects.filter(account=account)
        stocks = get_stock_info(all_stocks)
    if request.method == 'POST':
        print('trade:POST')
        if request.POST.get('action') == "search":
            symbol = request.POST.get("symbol")
            print('trade:POST symbol='+ symbol)
            stock_quote = yf.Ticker(symbol).info
            stock_quote=dict(
                exDividendDate=stock_quote["exDividendDate"] if stock_quote["exDividendDate"] else "",
                open=stock_quote["open"],
                ask=stock_quote["ask"],
                volume=stock_quote["volume"],
                fiftyTwoWeekHigh=stock_quote["fiftyTwoWeekHigh"],
                fiftyTwoWeekLow=stock_quote["fiftyTwoWeekLow"],
                fiftyTwoWeekChange=stock_quote["52WeekChange"],
                bid=stock_quote["bid"],
                previousClose=stock_quote["previousClose"],
                symbol=stock_quote["symbol"],
                sharesOutstanding=stock_quote["sharesOutstanding"],
                regularMarketPrice=stock_quote["regularMarketPrice"],
                dividendYield=stock_quote["dividendYield"] if stock_quote["dividendYield"] else "",
            )
            graph = get_stock_graph(symbol)
            return render( request, 'trade.html', {"stock_quote": stock_quote, "account": account, "stocks": stocks, "image": graph})
        if request.POST.get('action') == "sell":
            print('trade:POST action=sell')
            quantity = int(request.POST.get("quantity"))
            print('trade:POST quantity='+str(quantity))
 
            symbol = request.POST.get("stock")
            print('trade:POST symbol='+str(symbol))
 
            if symbol == "":
                return render( request, 'trade.html', {"account": account, "stocks": stocks})
            stock = Stock.objects.get(account=account, symbol=symbol)
            if quantity <= stock.quantity:   
                print('trade:quantity='+str(quantity))
                print('trade:stock.quantity='+str(stock.quantity))
 
                stock_quote = yf.Ticker(symbol).info
                sell_price = stock_quote["bid"]
                cash = quantity * sell_price
                account.balance += cash
                account.save()
                filtered_stock = Stock.objects.get(account=account, symbol=symbol)
                filtered_stock.quantity -= quantity
                filtered_stock.save()
                stocks = get_stock_info(Stock.objects.filter(account=account))
                message = "Succesfully sold stock"
            else:
                message = "That is more quantity than you have on your balance"
        if request.POST.get('action') == "buy":
            quantity = int(request.POST.get("quantity"))
            symbol = request.POST.get("symbol")
            account = Account.objects.get(user=request.user)
            stock_quote = yf.Ticker(symbol).info
            total_price = quantity*stock_quote["ask"]
            if account.balance > total_price:  
                stock = Stock.objects.filter(symbol=symbol, account=account)  
                if stock:
                    stock = stock[0]
                    stock.quantity += quantity
                    stock.save()
                else:
                    company_name = stock_quote["longName"]
                    # if the stock doesn't exist (by symbol and purchase price), it updates the quantity
                    stock = Stock.objects.create(symbol=symbol, quantity=quantity, account=account, company_name=company_name)
                # update the balance 
                account.balance -= total_price
                account.save()
                stocks = get_stock_info(Stock.objects.filter(account=account))
                message = "Succesfully bought stock"
            else:
                message = "Insufficient funds for buying stock"
    return render( request, 'trade.html', {"account": account, "stocks": stocks, "message": message})






