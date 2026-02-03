"""Comparison service for analyzing differences between datasets"""
from equipment_api.models import DataComparison, EquipmentDataset


class ComparisonService:
    """Handle dataset comparison logic"""
    
    @staticmethod
    def compare_datasets(dataset1, dataset2, user):
        """Compare two datasets and return detailed analysis"""
        
        # Get records from both datasets
        records1 = {r.equipment_name: r for r in dataset1.records.all()}
        records2 = {r.equipment_name: r for r in dataset2.records.all()}
        
        # Find common, added, and removed equipment
        common_names = set(records1.keys()) & set(records2.keys())
        added_names = set(records2.keys()) - set(records1.keys())
        removed_names = set(records1.keys()) - set(records2.keys())
        
        # Calculate differences for common equipment
        differences = []
        for name in common_names:
            r1 = records1[name]
            r2 = records2[name]
            
            diff = {
                'equipment_name': name,
                'flowrate_change': r2.flowrate - r1.flowrate,
                'flowrate_percent': ((r2.flowrate - r1.flowrate) / r1.flowrate * 100) if r1.flowrate != 0 else 0,
                'pressure_change': r2.pressure - r1.pressure,
                'pressure_percent': ((r2.pressure - r1.pressure) / r1.pressure * 100) if r1.pressure != 0 else 0,
                'temperature_change': r2.temperature - r1.temperature,
                'temperature_percent': ((r2.temperature - r1.temperature) / r1.temperature * 100) if r1.temperature != 0 else 0,
            }
            differences.append(diff)
        
        # Summary statistics
        comparison_result = {
            'dataset1_name': dataset1.filename,
            'dataset2_name': dataset2.filename,
            'total_equipment_1': dataset1.total_equipment,
            'total_equipment_2': dataset2.total_equipment,
            'common_equipment': len(common_names),
            'added_equipment': len(added_names),
            'removed_equipment': len(removed_names),
            'added_list': list(added_names),
            'removed_list': list(removed_names),
            'differences': differences,
            'summary': {
                'avg_flowrate_change': dataset2.avg_flowrate - dataset1.avg_flowrate,
                'avg_pressure_change': dataset2.avg_pressure - dataset1.avg_pressure,
                'avg_temperature_change': dataset2.avg_temperature - dataset1.avg_temperature,
            }
        }
        
        # Save comparison
        comparison = DataComparison.objects.create(
            user=user,
            dataset1=dataset1,
            dataset2=dataset2,
            comparison_result=comparison_result
        )
        
        return comparison_result
    
    @staticmethod
    def get_significant_changes(comparison_result, threshold=10):
        """Get equipment with significant parameter changes (>threshold%)"""
        significant = []
        
        for diff in comparison_result.get('differences', []):
            if (abs(diff['flowrate_percent']) > threshold or
                abs(diff['pressure_percent']) > threshold or
                abs(diff['temperature_percent']) > threshold):
                significant.append(diff)
        
        return significant
