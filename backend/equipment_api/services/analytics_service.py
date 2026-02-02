class AnalyticsService:
    """Calculate summary statistics from equipment data"""
    
    def calculate_summary(self, df):
        """
        Calculate averages and type distribution
        Returns: dict with summary stats
        """
        summary = {
            'total_equipment': len(df),
            'avg_flowrate': round(df['Flowrate'].mean(), 2),
            'avg_pressure': round(df['Pressure'].mean(), 2),
            'avg_temperature': round(df['Temperature'].mean(), 2),
            'type_distribution': df['Type'].value_counts().to_dict()
        }
        
        return summary
    
    def prepare_chart_data(self, dataset):
        """Prepare data for frontend charts"""
        records = dataset.records.all()
        
        # data for charts
        chart_data = {
            'type_distribution': dataset.type_distribution,
            'temperature_data': [
                {'name': r.equipment_name, 'value': r.temperature} 
                for r in records
            ],
            'pressure_data': [
                {'name': r.equipment_name, 'value': r.pressure} 
                for r in records
            ],
        }
        
        return chart_data
