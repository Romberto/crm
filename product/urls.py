from django.urls import path, re_path
from . import views

urlpatterns = [
    path('products/', views.ProductsView.as_view(), name='products'),
    path('add_product_group/', views.AddProductGroup.as_view(), name='add_product_group'),
    path('<int:id>', views.ProductListView.as_view(), name='product_group_list'),
    path('item/<int:id>', views.ProductItemView.as_view(), name='product_item'),
    path('product_group_edit/', views.edit_product_group, name='edit_product_group'),
    path('product_group_delete/', views.delete_product_group, name='delete_product_group'),
    path('add_product/',views.AddProductView.as_view(), name='add_product')

]