from django.db import models

# Model for table barang
class Barang(models.Model):
    nama_barang = models.CharField(max_length=100)
    harga_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    satuan = models.CharField(max_length=20)
    bulk_size = models.IntegerField(null=True, blank=True) # Allow blank or null values
    bulk_discount_rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nama_barang

    class Meta:
        db_table = 'barang'

class Transaksi(models.Model):
    tanggal_transaksi = models.DateTimeField(auto_now_add=True)
    total_harga = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transaksi #{self.id} - {self.tanggal_transaksi.strftime('%Y-%m-%d')}"

    class Meta:
        db_table = 'transaksi'

class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE, related_name='detail')
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.barang.nama_barang} x {self.qty}"

    class Meta:
        db_table = 'detail_transaksi'