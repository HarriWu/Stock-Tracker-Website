from django.forms import ModelForm
from .models import *


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['nasdaq_symbol', 'set_price']


class InfoForm(ModelForm):
    class Meta:
        model = Info
        fields = ['gmail_address','gmail_password','user_agent']
