import os
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string

from main.models import Pet, Category, Product, Help
from over_admin.models import CoverPhotos
from .forms import PhotoForm, PetForm, CategoryForm, ProductForm, LoginForm


def loginU(request):
    loginForm=LoginForm(request.POST or None)
    if request.method=="POST":
        if loginForm.is_valid():
            username = loginForm.cleaned_data.get('username')
            password = loginForm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Başarıyla giriş yaptınız.")
                    return redirect('admin_index')
    return render(request,"over_admin/login.html",{"form":loginForm})
def logoutU(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")

    return redirect("index")

@login_required(login_url="login")
def index(request):
    pet_count=Pet.objects.count()
    category_count=Category.objects.count()
    product_count=Product.objects.count()
    photos=CoverPhotos.objects.all()
    form=PhotoForm()
    return render(request,"over_admin/index.html",context={"pet_count":pet_count,"category_count":category_count,"product_count":product_count,"photos":photos,"form":form})

@login_required(login_url="login")
def change_photo_content(request,id):
    photo=CoverPhotos.objects.get(id=id)
    if request.method=="POST":
        first=request.POST.get("first")
        second=request.POST.get("second")
        photo.first_sentence=first
        photo.second_sentence=second
        photo.save()
        messages.success(request,"Açıklama başarıyla düzenlendi...")
        return redirect("admin_index")
    return render(request,"over_admin/change_photo_content.html",{"photo":photo})

@login_required(login_url="login")
def change_cover_photo(request,id):
    form=PhotoForm(data=request.POST ,files=request.FILES)
    if form.is_valid():
        photo = CoverPhotos.objects.get(id=id)

        file = form.cleaned_data.get("file")
        photo.file=file
        photo.save()
        messages.success(request, 'Fotoğraf başarıyla değişti..')  # <-

        return redirect("admin_index")
    return HttpResponse("Hata")

@login_required(login_url="login")
def pets(request):
    pets=Pet.objects.all()
    return render(request,"over_admin/pets.html",context={"pets":pets})

@login_required(login_url="login")
def delete_pet(request,id):
    pet=Pet.objects.get(id=id)
    pet.delete()
    messages.success(request, 'Kategori başarıyla silindi!')  # <-

    return redirect("admin_pets")

@login_required(login_url="login")
def add_pet(request):
    form=PetForm(data=request.POST ,files=request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Ana kategori başarıyla eklendi!')
            return redirect("admin_pets")
    return render(request,"over_admin/add_pet.html",context={"form":form})

@login_required(login_url="login")
def edit_pet(request,id):
    pet = get_object_or_404(Pet, id=id)
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)
    if form.is_valid():
        form.save()

        messages.success(request, "Ana kategori başarıyla güncellendi!")
        return redirect("admin_pets")

    return render(request, "over_admin/edit_pet.html", {"form": form})

@login_required(login_url="login")
def categories(request):
    pets=Pet.objects.all()

    return render(request,"over_admin/categories.html",context={"pets":pets})

@login_required(login_url="login")
def add_category(request):
    form=CategoryForm(data=request.POST)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Kategori başarıyla eklendi!")
            return redirect("admin_categories")
    return render(request,"over_admin/add_category.html",{"form":form})

@login_required(login_url="login")
def delete_category(request,petid,catid):
    cat=Category.objects.get(pet=petid,id=catid)
    cat.delete()
    messages.success(request,"Kategori başarıyla silindi!")
    return redirect("admin_categories")

@login_required(login_url="login")
def edit_category(request,petid,catid):
    cat=Category.objects.get(pet=petid,id=catid)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=cat)
    if form.is_valid():
        form.save()

        messages.success(request, "Kategori başarıyla güncellendi!")
        return redirect("admin_categories")

    return render(request, "over_admin/edit_categories.html", {"form": form})

@login_required(login_url="login")
def products(request):
    products=Product.objects.all().order_by("-created_date")
    return render(request,"over_admin/products.html",{"products":products})


@login_required(login_url="login")
def add_product(request):
    form=ProductForm(request.POST or None, request.FILES or None)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Ürün başarıyla eklendi!")
            return redirect("admin_products")
    return render(request,"over_admin/add_product.html",context={"form":form})

@login_required(login_url="login")
def get_relative_cat(request,id):
    pet=Pet.objects.get(id=id)
    cats=Category.objects.filter(pet=pet.id)
    html=render_to_string("over_admin/select_include.html",context={
        "request":request,
        "cats":cats,
    })
    return JsonResponse({"html":html})

@login_required(login_url="login")
def delete_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    messages.success(request,"Ürün başarıyla silindi!")
    return redirect("admin_products")

@login_required(login_url="login")
def edit_product(request,id):
    product=Product.objects.get(id=id)
    pet = product.category.pet
    initial = {"pet":pet}
    form = ProductForm(request.POST or None, request.FILES or None, instance=product,initial=initial)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Ürün başarıyla güncellendi!")
            return redirect("admin_products")
    return render(request,"over_admin/edit_product.html",context={"form":form})

@login_required(login_url="login")
def helps(request):
    helps=Help.objects.all().order_by("-created_date")
    return render(request,"over_admin/helps.html",context={"helps":helps})

@login_required(login_url="login")
def single_help(request,id):
    help=Help.objects.get(id=id)
    return render(request,"over_admin/single_help.html",context={"help":help})

@login_required(login_url="login")
def delete_help(request,id):
    help=Help.objects.get(id=id)
    help.delete()
    messages.success(request,"Mesaj başarıyla silindi!")
    return redirect("helps")
