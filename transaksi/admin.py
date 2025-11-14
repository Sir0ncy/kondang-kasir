from django.contrib import admin
from .models import Barang, Transaksi, DetailTransaksi

admin.site.register(Barang)
admin.site.register(Transaksi)
admin.site.register(DetailTransaksi)