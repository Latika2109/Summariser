"""Advanced feature API views"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    EquipmentDataset, EquipmentThreshold, DataComparison,
    SharedDataset, ScheduledReport, DataValidationReport
)
from .services.alert_service import AlertService
from .services.comparison_service import ComparisonService
from .services.validation_service import ValidationService
from .services.prediction_service import PredictionService
from .services.email_service import EmailService


@api_view(['POST'])
def set_thresholds(request):
    """Set alert thresholds for a parameter"""
    parameter = request.data.get('parameter')
    min_value = request.data.get('min_value')
    max_value = request.data.get('max_value')
    warning_threshold = request.data.get('warning_threshold')
    critical_threshold = request.data.get('critical_threshold')
    
    threshold, created = EquipmentThreshold.objects.update_or_create(
        user=request.user,
        parameter=parameter,
        defaults={
            'min_value': min_value,
            'max_value': max_value,
            'warning_threshold': warning_threshold,
            'critical_threshold': critical_threshold
        }
    )
    
    return Response({
        'id': threshold.id,
        'parameter': threshold.parameter,
        'min_value': threshold.min_value,
        'max_value': threshold.max_value,
        'warning_threshold': threshold.warning_threshold,
        'critical_threshold': threshold.critical_threshold,
        'created': created
    })


@api_view(['GET'])
def get_thresholds(request):
    """Get all thresholds for current user"""
    thresholds = EquipmentThreshold.objects.filter(user=request.user)
    data = [{
        'id': t.id,
        'parameter': t.parameter,
        'min_value': t.min_value,
        'max_value': t.max_value,
        'warning_threshold': t.warning_threshold,
        'critical_threshold': t.critical_threshold
    } for t in thresholds]
    
    return Response(data)


@api_view(['GET'])
def get_alerts(request, dataset_id):
    """Get alerts for a specific dataset"""
    dataset = get_object_or_404(EquipmentDataset, id=dataset_id, user=request.user)
    
    # Check alerts
    alerts = AlertService.check_alerts(dataset, request.user)
    summary = AlertService.get_alert_summary(dataset)
    
    return Response({
        'alerts': alerts,
        'summary': summary
    })


@api_view(['POST'])
def compare_datasets(request):
    """Compare two datasets"""
    dataset1_id = request.data.get('dataset1_id')
    dataset2_id = request.data.get('dataset2_id')
    
    dataset1 = get_object_or_404(EquipmentDataset, id=dataset1_id, user=request.user)
    dataset2 = get_object_or_404(EquipmentDataset, id=dataset2_id, user=request.user)
    
    comparison_result = ComparisonService.compare_datasets(dataset1, dataset2, request.user)
    significant_changes = ComparisonService.get_significant_changes(comparison_result)
    
    return Response({
        'comparison': comparison_result,
        'significant_changes': significant_changes
    })


@api_view(['GET'])
def get_comparisons(request):
    """Get all comparisons for current user"""
    comparisons = DataComparison.objects.filter(user=request.user).order_by('-created_at')[:10]
    data = [{
        'id': c.id,
        'dataset1': c.dataset1.filename,
        'dataset2': c.dataset2.filename,
        'created_at': c.created_at,
        'summary': c.comparison_result.get('summary', {})
    } for c in comparisons]
    
    return Response(data)


@api_view(['GET'])
def validate_dataset(request, dataset_id):
    """Get data quality validation report"""
    dataset = get_object_or_404(EquipmentDataset, id=dataset_id, user=request.user)
    
    # Generate or get validation report
    report = ValidationService.validate_dataset(dataset)
    
    if not report:
        return Response({'error': 'No data to validate'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'total_records': report.total_records,
        'missing_values': report.missing_values,
        'duplicate_records': report.duplicate_records,
        'outliers_count': report.outliers_count,
        'quality_score': report.quality_score,
        'details': report.validation_details
    })


@api_view(['GET'])
def get_predictions(request, dataset_id):
    """Get trend predictions for a dataset"""
    dataset = get_object_or_404(EquipmentDataset, id=dataset_id, user=request.user)
    
    # Generate predictions
    predictions = PredictionService.predict_trends(dataset)
    maintenance_alerts = PredictionService.get_maintenance_alerts(dataset)
    
    return Response({
        'predictions': predictions,
        'maintenance_alerts': maintenance_alerts
    })


@api_view(['POST'])
def share_dataset(request, dataset_id):
    """Share dataset with another user"""
    dataset = get_object_or_404(EquipmentDataset, id=dataset_id, user=request.user)
    username = request.data.get('username')
    can_edit = request.data.get('can_edit', False)
    
    try:
        from django.contrib.auth.models import User
        shared_with = User.objects.get(username=username)
        
        shared, created = SharedDataset.objects.get_or_create(
            dataset=dataset,
            owner=request.user,
            shared_with=shared_with,
            defaults={'can_edit': can_edit}
        )
        
        return Response({
            'success': True,
            'shared_with': username,
            'can_edit': can_edit,
            'created': created
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_shared_datasets(request):
    """Get datasets shared with current user"""
    shared = SharedDataset.objects.filter(shared_with=request.user)
    data = [{
        'id': s.dataset.id,
        'filename': s.dataset.filename,
        'owner': s.owner.username,
        'can_edit': s.can_edit,
        'shared_at': s.shared_at
    } for s in shared]
    
    return Response(data)


@api_view(['POST'])
def schedule_report(request):
    """Schedule automated email reports"""
    dataset_id = request.data.get('dataset_id')
    frequency = request.data.get('frequency')
    email = request.data.get('email', request.user.email)
    include_charts = request.data.get('include_charts', True)
    include_alerts = request.data.get('include_alerts', True)
    
    dataset = None
    if dataset_id:
        dataset = get_object_or_404(EquipmentDataset, id=dataset_id, user=request.user)
    
    scheduled = ScheduledReport.objects.create(
        user=request.user,
        dataset=dataset,
        frequency=frequency,
        email=email,
        include_charts=include_charts,
        include_alerts=include_alerts
    )
    
    return Response({
        'id': scheduled.id,
        'frequency': scheduled.frequency,
        'email': scheduled.email,
        'is_active': scheduled.is_active
    })


@api_view(['POST'])
def send_report_email(request, dataset_id):
    """Send dataset report via email"""
    try:
        dataset = get_object_or_404(EquipmentDataset, id=dataset_id, user=request.user)
        email = request.data.get('email', request.user.email)
        
        success, message = EmailService.send_report_email(dataset, email)
        
        if success:
            return Response({'success': True, 'message': message})
        else:
            return Response({'success': False, 'error': f'Failed to send email: {message}'}, 
                           status=status.HTTP_400_BAD_REQUEST) # Use 400 to distinguish from crash
                           
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'success': False, 
            'error': f'Server Error: {str(e)}',
            'trace': traceback.format_exc()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def batch_upload(request):
    """Upload multiple CSV files at once"""
    files = request.FILES.getlist('files')
    
    if not files:
        return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    results = []
    from .services.csv_processor import CSVProcessor
    
    for csv_file in files:
        try:
            if not csv_file.name.endswith('.csv'):
                results.append({
                    'filename': csv_file.name,
                    'success': False,
                    'error': 'Not a CSV file'
                })
                continue
            
            # Process CSV
            processor = CSVProcessor(csv_file)
            df = processor.process()
            
            # Create dataset (simplified - you'd want to use the full upload logic)
            from .services.analytics_service import AnalyticsService
            stats = AnalyticsService.calculate_summary_stats(df)
            type_dist = AnalyticsService.get_type_distribution(df)
            
            dataset = EquipmentDataset.objects.create(
                user=request.user,
                filename=csv_file.name,
                total_equipment=len(df),
                avg_flowrate=stats['avg_flowrate'],
                avg_pressure=stats['avg_pressure'],
                avg_temperature=stats['avg_temperature'],
                type_distribution=type_dist
            )
            
            # Create records
            for _, row in df.iterrows():
                EquipmentRecord.objects.create(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                )
            
            results.append({
                'filename': csv_file.name,
                'success': True,
                'dataset_id': dataset.id
            })
            
        except Exception as e:
            results.append({
                'filename': csv_file.name,
                'success': False,
                'error': str(e)
            })
    
    return Response({
        'total_files': len(files),
        'successful': len([r for r in results if r['success']]),
        'failed': len([r for r in results if not r['success']]),
        'results': results
    })
