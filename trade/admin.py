from django.contrib import admin

from trade.models import  TradeItemModel, TradeModel

# Register your models here.

class TradeItemAdmin(admin.ModelAdmin):
    list_filter = ('trade',)

class TradeAdmin(admin.ModelAdmin):
    list_filter = ('manager',)

admin.site.register(TradeItemModel, TradeItemAdmin)
admin.site.register(TradeModel, TradeAdmin)