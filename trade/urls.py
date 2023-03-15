from django.urls import path

from trade import views

urlpatterns = [
    path('all/', views.TradeAllView.as_view(), name='trade_all'),
    path('add/', views.TradeAddView.as_view(), name='trade_add'),
    path('detail/<int:id>', views.TradeDetailView.as_view(), name='trade_detail'),
    path('ajax_edit/', views.ajax_edit),
    path('ajax_text_vision/', views.ajax_text),
    path('ajax_text_message/', views.ajax_message),
    path('ajax_compare/', views.ajax_compare),
    path('ajax_logistic_valid/', views.ajax_logistic_valid),
    path('ajax_logistic_price/', views.ajax_logistic_price),
    path('ajax_get_agets/',views.ajax_get_agets),
    path('ajax_get_agent_form/', views.ajax_get_agent_form),
    path('ajax_post_agent_form/', views.ajax_post_agent_form),
    path('ajax_supplier_price/', views.ajax_supplier_price),
    path('ajax_supplier_count/',views.ajax_supplier_count),
    path('ajax_supplier_date/', views.ajax_supplier_date)
]