
from django.contrib import admin
from django.urls import path,include
from main import views
from over_admin import views as over
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',over.loginU,name="login"),
    path('logout',over.logoutU,name="logout"),
    path('',views.index,name="index"),
    path('iletisim',views.contact,name="contact"),
    path('yolla',views.add_help,name="add_help"),
    path('kategoriler',views.categories,name="categories"),
    path('urun/<int:id>',views.detail,name="detail"),
    path('kategori/<str:name>/<int:id>',views.filter_category,name="filter_category"),
    path('over_admin',over.index,name="admin_index"),
    path('change_cover_photo/<int:id>',over.change_cover_photo,name="change_cover"),
    path('ana_kategoriler',over.pets,name="admin_pets"),
    path('kategori_sil/<int:id>',over.delete_pet,name="delete_pet"),
    path('kategori_ekle',over.add_pet,name="add_pet"),
    path('kategori_duzenle/<int:id>',over.edit_pet,name="edit_pet"),
    path('alt_kategoriler',over.categories,name="admin_categories"),
    path('alt_kategori_ekle',over.add_category,name="add_category"),
    path('alt_kategori_sil/<int:petid>/<int:catid>',over.delete_category,name="delete_category"),
    path('alt_kategori_duzenle/<int:petid>/<int:catid>',over.edit_category,name="edit_category"),
    path('urunler',over.products,name="admin_products"),
    path('urun_ekle',over.add_product,name="add_product"),
    path('urun_sil/<int:id>',over.delete_product,name="delete_product"),
    path('urun_duzenle/<int:id>',over.edit_product,name="edit_product"),
    path('getir_alakali/<int:id>',over.get_relative_cat,name="get_relative_cat"),
    path('mesajlar',over.helps,name="helps"),
    path('mesaj/<int:id>',over.single_help,name="single_help"),
    path('sil_mesaj/<int:id>',over.delete_help,name="delete_help")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
