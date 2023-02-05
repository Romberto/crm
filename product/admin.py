from django.contrib import admin

from product.models import GroupProductModel, ProductModel, ProductPackagingModel


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('product_name', 'product_group')

admin.site.register(GroupProductModel)
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(ProductPackagingModel)


