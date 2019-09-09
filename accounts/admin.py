from django.contrib import admin

# Register your models here.
from StockPriceTracker.models import Stock, Info

admin.site.register(Info)
admin.site.register(Stock)