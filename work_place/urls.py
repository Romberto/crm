from django.urls import path

from work_place import views

urlpatterns = [
    path('', views.WorkPlaceView.as_view(), name='work_place'),


]