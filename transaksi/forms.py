from django import forms
from .models import Barang

class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = ['nama_barang', 'harga_per_unit', 'satuan', 'bulk_size', 'bulk_discount_rate']
        widgets = {
            'nama_barang': forms.TextInput(attrs={'class': 'form-control'}),
            'harga_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'satuan': forms.TextInput(attrs={'class': 'form-control'}),
            'bulk_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'bulk_discount_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    