from django.urls import path

from trade import views

urlpatterns = [
    path('all/', views.TradeAllView.as_view(), name='trade_all'),
    path('add/', views.TradeAddView.as_view(), name='trade_add'),
    path('detail/<int:id>', views.TradeDetailView.as_view(), name='trade_detail'),
    path('ajax_edit/', views.ajax_edit)
]