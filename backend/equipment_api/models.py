from django.db import models
from django.contrib.auth.models import User

class EquipmentDataset(models.Model):
    """Stores metadata and summary for each CSV upload"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    
    # summary stats
    total_equipment = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField()  # stores dict of equipment types and counts
    
    # hierarchy
    plant = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentRecord(models.Model):
    """Individual equipment data from CSV"""
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    # alert status
    has_alert = models.BooleanField(default=False)
    alert_level = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('warning', 'Warning'),
        ('critical', 'Critical')
    ], default='normal')
    
    def __str__(self):
        return self.equipment_name


class EquipmentThreshold(models.Model):
    """User-defined thresholds for alerts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50, choices=[
        ('flowrate', 'Flowrate'),
        ('pressure', 'Pressure'),
        ('temperature', 'Temperature')
    ])
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    warning_threshold = models.FloatField(null=True, blank=True)
    critical_threshold = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'parameter']
    
    def __str__(self):
        return f"{self.user.username} - {self.parameter}"


class DataComparison(models.Model):
    """Stores comparison between two datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset1 = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='comparisons_as_first')
    dataset2 = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='comparisons_as_second')
    comparison_result = models.JSONField()  # stores detailed comparison data
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comparison: {self.dataset1.filename} vs {self.dataset2.filename}"


class SharedDataset(models.Model):
    """Collaboration - share datasets with other users"""
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_datasets')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_datasets')
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['dataset', 'shared_with']
    
    def __str__(self):
        return f"{self.dataset.filename} shared with {self.shared_with.username}"


class ScheduledReport(models.Model):
    """Email automation for reports"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ])
    email = models.EmailField()
    include_charts = models.BooleanField(default=True)
    include_alerts = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.frequency} report"


class DataValidationReport(models.Model):
    """Data quality metrics"""
    dataset = models.OneToOneField(EquipmentDataset, on_delete=models.CASCADE)
    total_records = models.IntegerField()
    missing_values = models.IntegerField(default=0)
    duplicate_records = models.IntegerField(default=0)
    outliers_count = models.IntegerField(default=0)
    quality_score = models.FloatField()  # 0-100
    validation_details = models.JSONField()  # detailed breakdown
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Validation: {self.dataset.filename} ({self.quality_score}%)"


class PredictionResult(models.Model):
    """Store prediction/trend analysis results"""
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE)
    equipment_record = models.ForeignKey(EquipmentRecord, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50)
    predicted_value = models.FloatField()
    confidence = models.FloatField()  # 0-1
    prediction_date = models.DateField()
    trend = models.CharField(max_length=20, choices=[
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.equipment_record.equipment_name} - {self.parameter} prediction"
