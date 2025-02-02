from django.contrib import admin
from .models import FillLevel, AirQuality, GasDetection, BinState

admin.site.register(FillLevel)
admin.site.register(AirQuality)
admin.site.register(GasDetection)
admin.site.register(BinState)
