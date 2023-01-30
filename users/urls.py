from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from . import views
from .views import ApiUserView

router = SimpleRouter()
router.register('api_user', ApiUserView)

urlpatterns = [
    path('', views.UserCRMView.as_view(), name='users'),

    ]

urlpatterns += router.urls