from django.urls import path

from work_place import views

urlpatterns = [
    path('', views.WorkPlaceView.as_view(), name='work_place'),
    path('agreement/<int:id>/',views.AgreementView.as_view(),name='work_agreement'),
    path('ajax_stamp/',views.ajax_stamp),
    path('ajax_agreement/', views.ajax_agreement)


]