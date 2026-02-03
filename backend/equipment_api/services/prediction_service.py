"""Prediction service for trend analysis and forecasting"""
from equipment_api.models import PredictionResult
from datetime import datetime, timedelta
import numpy as np


class PredictionService:
    """Handle predictive maintenance and trend analysis"""
    
    @staticmethod
    def predict_trends(dataset):
        """Analyze trends for all equipment in dataset"""
        predictions = []
        
        for record in dataset.records.all():
            # Predict for each parameter
            for param in ['flowrate', 'pressure', 'temperature']:
                prediction = PredictionService._simple_trend_prediction(
                    record, param, dataset
                )
                if prediction:
                    predictions.append(prediction)
        
        return predictions
    
    @staticmethod
    def _simple_trend_prediction(record, parameter, dataset):
        """Simple linear trend prediction based on historical data"""
        # Get historical data for this equipment (if available)
        # For now, use simple heuristics based on current values
        
        current_value = getattr(record, parameter)
        
        # Calculate average for this parameter across dataset
        records = dataset.records.all()
        values = [getattr(r, parameter) for r in records]
        avg_value = np.mean(values)
        std_value = np.std(values)
        
        # Determine trend
        if current_value > avg_value + std_value:
            trend = 'increasing'
            predicted_value = current_value * 1.05  # 5% increase
            confidence = 0.7
        elif current_value < avg_value - std_value:
            trend = 'decreasing'
            predicted_value = current_value * 0.95  # 5% decrease
            confidence = 0.7
        else:
            trend = 'stable'
            predicted_value = current_value
            confidence = 0.85
        
        # Prediction for 7 days from now
        prediction_date = datetime.now().date() + timedelta(days=7)
        
        # Create prediction record
        prediction = PredictionResult.objects.create(
            dataset=dataset,
            equipment_record=record,
            parameter=parameter,
            predicted_value=predicted_value,
            confidence=confidence,
            prediction_date=prediction_date,
            trend=trend
        )
        
        return {
            'equipment_name': record.equipment_name,
            'parameter': parameter,
            'current_value': current_value,
            'predicted_value': predicted_value,
            'trend': trend,
            'confidence': confidence,
            'prediction_date': str(prediction_date)
        }
    
    @staticmethod
    def get_maintenance_alerts(dataset):
        """Get equipment that may need maintenance based on predictions"""
        predictions = PredictionResult.objects.filter(dataset=dataset)
        alerts = []
        
        for pred in predictions:
            # Flag equipment with increasing temperature or pressure
            if pred.parameter in ['temperature', 'pressure'] and pred.trend == 'increasing':
                alerts.append({
                    'equipment_name': pred.equipment_record.equipment_name,
                    'parameter': pred.parameter,
                    'current': getattr(pred.equipment_record, pred.parameter),
                    'predicted': pred.predicted_value,
                    'confidence': pred.confidence,
                    'recommendation': f'Monitor {pred.parameter} - showing increasing trend'
                })
        
        return alerts
