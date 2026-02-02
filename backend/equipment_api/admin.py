from django.contrib import admin
from .models import EquipmentDataset, EquipmentRecord


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    """Admin interface for equipment datasets"""
    list_display = ['filename', 'user', 'uploaded_at', 'total_equipment', 'avg_temperature']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['filename', 'user__username']
    readonly_fields = ['uploaded_at', 'total_equipment', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    date_hierarchy = 'uploaded_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(EquipmentRecord)
class EquipmentRecordAdmin(admin.ModelAdmin):
    """Admin interface for individual equipment records"""
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset__uploaded_at']
    search_fields = ['equipment_name', 'equipment_type']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('dataset', 'dataset__user')
