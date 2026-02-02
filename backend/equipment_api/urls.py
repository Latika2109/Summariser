from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'datasets', views.EquipmentDatasetViewSet, basename='dataset')

urlpatterns = [
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('upload/', views.upload_csv, name='upload'),
    path('', include(router.urls)),
]
