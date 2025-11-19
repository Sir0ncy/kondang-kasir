from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Barang
from .forms import BarangForm

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def kasir(request):
    products = Barang.objects.all()
    return render(request, 'kasir.html', {
        'products': products
    })

def produk_list(request):
    produk_list = Barang.objects.all()
    return render(request, "produk/list.html", {"produk_list": produk_list})

def produk_create(request):
    form = BarangForm()

    if request.method == 'POST':
        form = BarangForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produk_list")
        
    return render(request, "produk/form.html", {"form": form, "title": "Tambah Produk"}) 

def produk_edit(request, id):
    barang = get_object_or_404(Barang, id=id)
    form = BarangForm(instance=barang)

    if request.method == "POST":
        form = BarangForm(request.POST, instance=barang)
        if form.is_valid():
            form.save()
            return redirect("produk_list")

    return render(request, "produk/form.html", {"form": form, "title": "Edit Produk"})

def produk_delete(request, id):
    barang = get_object_or_404(Barang, id=id)
    barang.delete()
    return redirect("produk_list")
