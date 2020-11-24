from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from main.models import Pet, Product, Category, Help
from over_admin.models import CoverPhotos


def index(request):
    product_count = None
    pets=Pet.objects.all()
    covers=CoverPhotos.objects.all()
    arama = request.GET.get("search", None)
    search=False
    searched=""
    if arama:
        products = Product.objects.filter(
            Q(name__icontains=arama) |
            Q(detail__icontains=arama) |
            Q(brand__icontains=arama) |
            Q(category__name__icontains=arama) |
            Q(category__pet__name__icontains=arama)
        )
        search=True
        searched=arama
        product_count = products.count()

    else:
        query=Product.objects.all().order_by("-created_date")
        page = request.GET.get('page', 1)
        paginator = Paginator(query, 16)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    return render(request,"index.html",context={"pets":pets,"products":products,"search":search,"product_count":product_count,"searched":searched,"covers":covers})

def contact(request):
    arama = request.GET.get("search", None)
    if arama:
        return redirect(reverse('index') + '?search={}'.format(arama))
    return render(request,"contact.html")

def categories(request):
    pets=Pet.objects.all()
    arama = request.GET.get("search", None)
    if arama:
        return redirect(reverse('index') + '?search={}'.format(arama))
    return render(request,"categories.html",context={"pets":pets})

def detail(request,id):
    product=Product.objects.get(id=id)
    arama = request.GET.get("search", None)
    if arama:
        return redirect(reverse('index') + '?search={}'.format(arama))
    return render(request,"detail.html",context={"product":product})

def filter_category(request,name,id):
    arama = request.GET.get("search", None)
    if arama:
        return redirect(reverse('index') + '?search={}'.format(arama))
    pets=Pet.objects.all()
    query = Product.objects.filter(category__pet__name=name,category=id).all()
    covers=CoverPhotos.objects.all()
    product_count = Product.objects.filter(category=id).count()

    page = request.GET.get('page', 1)
    paginator = Paginator(query, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,"index.html",context={"pets":pets,"products":products,"searched":False,"covers":covers,"product_count":product_count,"is_category":True,"category":Category.objects.get(id=id)})

def add_help(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    message=request.POST.get("message")
    print(name)
    Help.objects.create(name=name,email=email,message=message)
    messages.success(request,"Mesajınız başarıyla gönderildi! En yakın zamanda size geri dönüş sağlayacağız...")
    return redirect("index")
