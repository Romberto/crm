from django.contrib import admin

from trade.models import TradeItemModel, TradeModel, TradeAgentItem, TradeAgent


# Register your models here.

class TradeItemAdmin(admin.ModelAdmin):
    list_filter = ('trade',)

class TradeAdmin(admin.ModelAdmin):
    list_filter = ('manager',)

class TradeAdminAgentItems(admin.ModelAdmin):
    list_filter = ('trade_agent',)

admin.site.register(TradeItemModel, TradeItemAdmin)
admin.site.register(TradeModel, TradeAdmin)
admin.site.register(TradeAgentItem, TradeAdminAgentItems)
admin.site.register(TradeAgent)