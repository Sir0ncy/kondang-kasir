from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('kasir/', views.kasir, name='kasir'),

    # Produk/Barang CRUD
    path('produk/', views.produk_list, name='produk_list'),
    path('produk/tambah/', views.produk_create, name='produk_create'),
    path('produk/edit/<int:id>', views.produk_edit, name='produk_edit'),
    path('produk/hapus/<int:id>', views.produk_delete, name='produk_delete'),

]