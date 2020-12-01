"""djangostocktrader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.home, name="home"),   #localhost:8000/   -->> views.home()
        path('login', views.login, name="login"),
        path('login_user' , views.login_user , name = 'login_user'),
        path('logout', views.logout, name="logout"),
        path('signup/', views.signup, name="signup"),
        path('about', views.about, name="about"),
        path('contact', views.contact, name="contact"),
        path('product', views.product, name="product"),  #localhost:8000/product --> views.product()
        path('getPrice/<id>', views.getPrice), #localhost:8000/getPrice/1 or something
        path('add_stock.html', views.add_stock, name="add_stock"),
        path('delete/<stock_id>', views.delete, name="delete"),
        path('delete_stock.html', views.delete_stock, name="delete_stock"),
        path('ticker_chart.html', views.ticker_chart, name="ticker_chart"),
        path('stockproduct', views.stockproduct, name="stockproduct"),
        path('my_stock_plot_view', views.my_stock_plot_view, name="my_stock_plot_view"),
        path('trading.html', views.trading, name="trading"),
        path('getTotalCost', views.getTotalCost, name="getTotalCost"),
        path('bankaccount', views.bankaccount, name="bankaccount"),
       # path('fetchStockData', views.fetchStockData, name="fetchStockData"),
        path('bankroll', views.bankroll, name="bankroll"),

]       + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
