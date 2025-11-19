from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from .models import Barang
from .forms import BarangForm
from .models import Barang, Transaksi
from .models import Transaksi, DetailTransaksi

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def kasir(request):
    products = Barang.objects.all()
    return render(request, 'kasir.html', {
        'products': products
    })

def riwayat(request):
    transaksi_list = Transaksi.objects.all().order_by('-tanggal_transaksi')
    return render(request, 'riwayat.html', {
        'transaksi_list': transaksi_list
    })
    
def laporan_penjualan(request):

    total_transaksi = Transaksi.objects.count()

    total_item = DetailTransaksi.objects.aggregate(
        total=Sum('qty')
    )['total'] or 0

    total_pendapatan = Transaksi.objects.aggregate(
        total=Sum('total_harga')
    )['total'] or 0

    penjualan_barang = (
        DetailTransaksi.objects
        .values('barang__nama_barang')
        .annotate(
            total_qty=Sum('qty'),
            total_pendapatan=Sum('subtotal')
        )
        .order_by('-total_qty')
    )

    detail_list = DetailTransaksi.objects.select_related("transaksi", "barang")

    return render(request, "laporan.html", {
        'total_transaksi': total_transaksi,
        'total_item': total_item,
        'total_pendapatan': total_pendapatan,
        'penjualan_barang': penjualan_barang,
        'detail_list': detail_list,
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
