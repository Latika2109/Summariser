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
    
    def analyze_health(self, dataset):
        """"
        Calculate health scores and power efficiency
        """
        records = dataset.records.all()
        analysis = []
        
        # Calculate dataset averages (baselines)
        avg_flow = dataset.avg_flowrate or 1
        avg_press = dataset.avg_pressure or 1
        avg_temp = dataset.avg_temperature or 1
        
        for r in records:
            # 1. Hydraulic Power Calculation (Flow * Pressure proxy)
            # Higher is not necessarily 'better' or 'worse', but indicates load
            power_index = r.flowrate * r.pressure
            
            # 2. Health Score Calculation
            # 100 - average deviation % of all parameters
            # Lower deviation = Higher Health
            
            flow_dev = abs(r.flowrate - avg_flow) / avg_flow
            press_dev = abs(r.pressure - avg_press) / avg_press
            temp_dev = abs(r.temperature - avg_temp) / avg_temp
            
            avg_dev = (flow_dev + press_dev + temp_dev) / 3
            health_score = max(0, 100 - (avg_dev * 100)) # Simple 0-100 score
            
            status = 'Good'
            if health_score < 70: status = 'Warning'
            if health_score < 50: status = 'Critical'
            
            analysis.append({
                'id': r.id,
                'name': r.equipment_name,
                'type': r.equipment_type,
                'health_score': round(health_score, 1),
                'status': status,
                'power_index': round(power_index, 2),
                'flowrate': r.flowrate,
                'pressure': r.pressure,
                'temperature': r.temperature
            })
            
        return sorted(analysis, key=lambda x: x['health_score']) # Sort by lowest health (riskiest first)

    def analyze_root_cause(self, record):
        """
        AI-driven root cause analysis (simulated but logic-backed)
        """
        causes = []
        
        # High Pressure Logic
        if record.pressure > 18:
            causes.append("Excessive system pressure detected (Potential Blockage)")
            if record.temperature > 50:
                causes.append("Co-occurring thermal spike indicates pump overheating")
        
        # Low Flow Logic
        if record.flowrate < 100:
            causes.append("Low flowrate indicates potential leak or valve failure")
        
        # High Temp Logic
        if record.temperature > 80:
            causes.append("Critical thermal threshold exceeded (Coolant Failure)")
            
        # Default if no specific logic hits but alert triggered
        if not causes:
            causes.append("Deviation from historical baseline detected")
            if record.pressure > 10:
                causes.append("Pressure variance observed")
                
        return causes
