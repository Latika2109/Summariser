"""Alert service for threshold checking and equipment alerts"""
from equipment_api.models import EquipmentThreshold, EquipmentRecord


class AlertService:
    """Handle equipment alert logic"""
    
    @staticmethod
    def check_alerts(dataset, user):
        """Check all equipment records against user thresholds"""
        thresholds = EquipmentThreshold.objects.filter(user=user)
        alerts = []
        
        for record in dataset.records.all():
            alert_info = AlertService._check_record(record, thresholds)
            if alert_info:
                alerts.append(alert_info)
                # Update record alert status
                record.has_alert = True
                record.alert_level = alert_info['level']
                record.save()
        
        return alerts
    
    @staticmethod
    def _check_record(record, thresholds):
        """Check single record against thresholds"""
        for threshold in thresholds:
            param_value = getattr(record, threshold.parameter)
            
            # Check critical threshold
            if threshold.critical_threshold and param_value > threshold.critical_threshold:
                return {
                    'equipment_name': record.equipment_name,
                    'parameter': threshold.parameter,
                    'value': param_value,
                    'threshold': threshold.critical_threshold,
                    'level': 'critical',
                    'message': f'{threshold.parameter.title()} critically high: {param_value}'
                }
            
            # Check warning threshold
            if threshold.warning_threshold and param_value > threshold.warning_threshold:
                return {
                    'equipment_name': record.equipment_name,
                    'parameter': threshold.parameter,
                    'value': param_value,
                    'threshold': threshold.warning_threshold,
                    'level': 'warning',
                    'message': f'{threshold.parameter.title()} warning: {param_value}'
                }
            
            # Check min/max bounds
            if threshold.min_value and param_value < threshold.min_value:
                return {
                    'equipment_name': record.equipment_name,
                    'parameter': threshold.parameter,
                    'value': param_value,
                    'threshold': threshold.min_value,
                    'level': 'warning',
                    'message': f'{threshold.parameter.title()} below minimum: {param_value}'
                }
            
            if threshold.max_value and param_value > threshold.max_value:
                return {
                    'equipment_name': record.equipment_name,
                    'parameter': threshold.parameter,
                    'value': param_value,
                    'threshold': threshold.max_value,
                    'level': 'warning',
                    'message': f'{threshold.parameter.title()} above maximum: {param_value}'
                }
        
        return None
    
    @staticmethod
    def get_alert_summary(dataset):
        """Get summary of alerts for a dataset"""
        records = dataset.records.all()
        total = records.count()
        critical = records.filter(alert_level='critical').count()
        warning = records.filter(alert_level='warning').count()
        normal = records.filter(alert_level='normal').count()
        
        return {
            'total_equipment': total,
            'critical_alerts': critical,
            'warning_alerts': warning,
            'normal': normal,
            'alert_percentage': ((critical + warning) / total * 100) if total > 0 else 0
        }
