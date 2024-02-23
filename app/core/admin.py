from django.contrib import admin
from core.models import Currency, CurrencyExchangeRate

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
