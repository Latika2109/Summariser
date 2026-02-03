"""Validation service for data quality checks"""
from equipment_api.models import DataValidationReport
import pandas as pd


class ValidationService:
    """Handle data quality validation"""
    
    @staticmethod
    def validate_dataset(dataset):
        """Perform comprehensive data quality checks"""
        records = dataset.records.all()
        total_records = records.count()
        
        if total_records == 0:
            return None
        
        # Convert to DataFrame for analysis
        data = list(records.values('flowrate', 'pressure', 'temperature', 'equipment_name'))
        df = pd.DataFrame(data)
        
        # Check for missing values (shouldn't happen with our validation, but good to check)
        missing_values = df.isnull().sum().sum()
        
        # Check for duplicates
        duplicate_records = df.duplicated(subset=['equipment_name']).sum()
        
        # Detect outliers using IQR method
        outliers_count = 0
        outlier_details = []
        
        for column in ['flowrate', 'pressure', 'temperature']:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            outliers_count += len(outliers)
            
            if len(outliers) > 0:
                outlier_details.append({
                    'parameter': column,
                    'count': len(outliers),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'equipment': outliers['equipment_name'].tolist()[:5]  # First 5
                })
        
        # Calculate quality score
        quality_score = 100
        quality_score -= (missing_values / (total_records * 3)) * 20  # Max -20 for missing
        quality_score -= (duplicate_records / total_records) * 30  # Max -30 for duplicates
        quality_score -= min((outliers_count / total_records) * 50, 50)  # Max -50 for outliers
        quality_score = max(0, quality_score)
        
        # Validation details
        validation_details = {
            'missing_values_breakdown': {
                'flowrate': int(df['flowrate'].isnull().sum()),
                'pressure': int(df['pressure'].isnull().sum()),
                'temperature': int(df['temperature'].isnull().sum())
            },
            'duplicate_equipment': int(duplicate_records),
            'outliers': outlier_details,
            'statistics': {
                'flowrate': {
                    'min': float(df['flowrate'].min()),
                    'max': float(df['flowrate'].max()),
                    'mean': float(df['flowrate'].mean()),
                    'std': float(df['flowrate'].std())
                },
                'pressure': {
                    'min': float(df['pressure'].min()),
                    'max': float(df['pressure'].max()),
                    'mean': float(df['pressure'].mean()),
                    'std': float(df['pressure'].std())
                },
                'temperature': {
                    'min': float(df['temperature'].min()),
                    'max': float(df['temperature'].max()),
                    'mean': float(df['temperature'].mean()),
                    'std': float(df['temperature'].std())
                }
            }
        }
        
        # Create or update validation report
        report, created = DataValidationReport.objects.update_or_create(
            dataset=dataset,
            defaults={
                'total_records': total_records,
                'missing_values': missing_values,
                'duplicate_records': duplicate_records,
                'outliers_count': outliers_count,
                'quality_score': quality_score,
                'validation_details': validation_details
            }
        )
        
        return report
