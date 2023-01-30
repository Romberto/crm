from django.urls import path

from client import views

urlpatterns = [
    path('client_all/', views.AllClientsView.as_view(), name='all_clients'),
    path('client_detail/<int:id_client>', views.DetailClientView.as_view(), name='detail_client'),
    path('client_add/', views.AddClientView.as_view(), name="add_client"),
    path('client_delete/<int:id_client>', views.ClientDeleteView.as_view(), name='delete_client')
]