from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import advanced_views

router = DefaultRouter()
router.register(r'datasets', views.EquipmentDatasetViewSet, basename='dataset')

urlpatterns = [
    # Authentication
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    
    # Basic upload
    path('upload/', views.upload_csv, name='upload'),
    
    # Advanced features - Alerts
    path('thresholds/', advanced_views.get_thresholds, name='get-thresholds'),
    path('thresholds/set/', advanced_views.set_thresholds, name='set-thresholds'),
    path('datasets/<int:dataset_id>/alerts/', advanced_views.get_alerts, name='get-alerts'),
    
    # Comparison
    path('compare/', advanced_views.compare_datasets, name='compare-datasets'),
    path('comparisons/', advanced_views.get_comparisons, name='get-comparisons'),
    
    # Validation
    path('datasets/<int:dataset_id>/validate/', advanced_views.validate_dataset, name='validate-dataset'),
    
    # Predictions
    path('datasets/<int:dataset_id>/predictions/', advanced_views.get_predictions, name='get-predictions'),
    
    # Collaboration
    path('datasets/<int:dataset_id>/share/', advanced_views.share_dataset, name='share-dataset'),
    path('shared/', advanced_views.get_shared_datasets, name='get-shared-datasets'),
    
    # Email & Scheduling
    path('schedule-report/', advanced_views.schedule_report, name='schedule-report'),
    path('datasets/<int:dataset_id>/send-email/', advanced_views.send_report_email, name='send-email'),
    
    # Batch upload
    path('batch-upload/', advanced_views.batch_upload, name='batch-upload'),
    
    # Router URLs
    path('', include(router.urls)),
]
