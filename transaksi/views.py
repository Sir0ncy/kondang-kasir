from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from .models import Barang
from .forms import BarangForm
from .models import Barang, Transaksi
from .models import Transaksi, DetailTransaksi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
def transaksi_delete(request, id):
    transaksi = get_object_or_404(Transaksi, id=id)
    transaksi.delete()
    return redirect("riwayat")

def transaksi_edit(request, id):
    transaksi = get_object_or_404(Transaksi, id=id)
    detail_items = DetailTransaksi.objects.filter(transaksi=transaksi)

    if request.method == "POST":
        total_harga_baru = request.POST.get("total_harga")

        if total_harga_baru:
            transaksi.total_harga = total_harga_baru
            transaksi.save()

        return redirect("riwayat")

    return render(request, "transaksi/edit.html", {
        "transaksi": transaksi,
        "detail_items": detail_items
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

@csrf_exempt
@login_required
def checkout(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

    data = json.loads(request.body)
    cart = data.get("cart", {})

    if not cart:
        return JsonResponse({"status": "error", "message": "Keranjang kosong"}, status=400)

    # Create transaksi
    transaksi = Transaksi.objects.create(total_harga=0)

    total_harga_final = 0

    # Process each item in cart
    for pid, item in cart.items():
        barang = Barang.objects.get(id=pid)
        qty = float(item["qty"])

        # Load bulk discount
        bulk_size = barang.bulk_size or 0
        bulk_discount = barang.bulk_discount_rate or 0

        harga_normal = float(barang.harga_per_unit)

        # Bulk calculation
        if bulk_size > 0 and qty >= bulk_size:
            bulk_groups = int(qty // bulk_size)
            remainder = qty % bulk_size

            bulk_price = harga_normal * bulk_size * (1 - bulk_discount / 100)
            subtotal = (bulk_groups * bulk_price) + (remainder * harga_normal)

        else:
            subtotal = qty * harga_normal

        total_harga_final += subtotal

        DetailTransaksi.objects.create(
            transaksi=transaksi,
            barang=barang,
            qty=qty,
            harga_satuan=barang.harga_per_unit,
            subtotal=subtotal
        )

    transaksi.total_harga = total_harga_final
    transaksi.save()

    return JsonResponse({
        "status": "success",
        "message": "Transaksi berhasil dicatat",
        "redirect": "/kasir/"
    })
