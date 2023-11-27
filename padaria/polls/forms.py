# forms.py
from django import forms

class OrderForm(forms.Form):
    clientName = forms.CharField(max_length=40)
    orderProduct = forms.IntegerField()
