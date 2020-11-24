from django import forms
from django.contrib.auth import authenticate

from main.models import Pet, Category, Product
from over_admin.models import CoverPhotos


class PhotoForm(forms.ModelForm):
    class Meta:
        model = CoverPhotos
        fields = ["file"]

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs = {'class': "btn btn-primary w-100","required":"required"}

class PetForm(forms.ModelForm):
    class Meta:
        model=Pet
        fields=["name","file"]
    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs = {'class': "btn btn-primary w-100"}
        self.fields["name"].widget.attrs = {'class': "form-control"}

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ["name", "pet"]
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs = {'class': "form-control","required":"required"}
        self.fields["pet"].widget.attrs = {'class': "form-control","required":"required"}

class ProductForm(forms.ModelForm):
    pet = forms.ModelChoiceField(queryset=Pet.objects.all(),blank=False)
    class Meta:
        model=Product
        fields=["file","name","brand","category","price","detail","weight","pet"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields["file"].widget.attrs = {'class': "btn btn-primary w-100"}
        self.fields["price"].widget.attrs = {'step': "any",'class': 'form-control'}
        self.fields["weight"].widget.attrs = {'step': "any",'class': 'form-control'}
        self.fields["category"].widget.attrs = {'class': "form-control","required":"required"}

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Kullanıcı Adı/E-Posta',
                               widget=forms.TextInput(attrs={'class': 'form-control',"placeholder":"Kullanıcı Adı/E-Posta"}))
    password = forms.CharField(required=True, max_length=50, label='Parola',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder":"Parola"}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Kullanıcı Adı veya Şifre Hatalı')

