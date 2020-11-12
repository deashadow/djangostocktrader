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

urlpatterns = [
        path('', views.home),   #localhost:8000/   -->> views.home()
        path('about', views.about),
        path('contact', views.contact),
        path('product', views.product),  #localhost:8000/product --> views.product()
        path('products', views.products),
        path('getPrice/<id>', views.getPrice), #localhost:8000/getPrice/1 or something

]
