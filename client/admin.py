from django.contrib import admin

from client.models import ClientModel


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_filter = ('owner_manager',)


admin.site.register(ClientModel, ClientAdmin)
