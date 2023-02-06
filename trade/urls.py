from django.urls import path

from trade import views

urlpatterns = [
    path('all/', views.TradeAllView.as_view(), name='trade_all'),


]