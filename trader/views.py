from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product
from .forms import ProductForm
import yfinance as yf

# Create your views here.



def home( request):
    return render( request, 'home.html')

def about( request):
    return render( request, 'about.html')

def contact( request):
    return render( request, 'contact.html')

def products( request):
    products = Product.objects.all();
    context = { 'products' : products}
    return render( request, 'products.html', context)

def product( request):
    if request.method == 'POST':
        productForm = ProductForm( request.POST)
        if productForm.is_valid() == False:
            return HttpResponse( productForm.errors)
        productForm.save();
        return redirect("/products");
    elif request.method == 'GET':
        productForm = ProductForm()
    context = { 'productForm' : productForm}
    return render( request, 'product.html', context)


def getPrice( request, id):
    ticker = yf.Ticker(id)
    retval = { "price" : ticker.info['regularMarketPrice']}
    return JsonResponse(retval)
    


