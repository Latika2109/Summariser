from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import EquipmentDataset, EquipmentRecord
from .serializers import (
    EquipmentDatasetSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer
)
from .services.csv_processor import CSVProcessor
from .services.analytics_service import AnalyticsService
from .services.pdf_service import PDFService
from .services.excel_service import ExcelExportService


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """User login"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_csv(request):
    """Handle CSV upload and processing"""
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    csv_file = request.FILES['file']
    
    # validate file extension
    if not csv_file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # process CSV
        processor = CSVProcessor()
        df = processor.validate_and_parse(csv_file)
        
        # calculate summary stats
        analytics = AnalyticsService()
        summary = analytics.calculate_summary(df)
        
        # create dataset record
        dataset = EquipmentDataset.objects.create(
            user=request.user,
            filename=csv_file.name,
            total_equipment=summary['total_equipment'],
            avg_flowrate=summary['avg_flowrate'],
            avg_pressure=summary['avg_pressure'],
            avg_temperature=summary['avg_temperature'],
            type_distribution=summary['type_distribution']
        )
        
        # create individual equipment records
        for _, row in df.iterrows():
            EquipmentRecord.objects.create(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )
        
        # keep only last 20 datasets per user
        user_datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-uploaded_at')
        if user_datasets.count() > 20:
            # delete oldest datasets
            datasets_to_delete = user_datasets[20:]
            for old_dataset in datasets_to_delete:
                old_dataset.delete()
        
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class EquipmentDatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing and retrieving datasets"""
    serializer_class = EquipmentDatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # return only user's datasets
        return EquipmentDataset.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """Generate PDF report for a dataset"""
        dataset = self.get_object()
        
        try:
            pdf_service = PDFService()
            pdf_buffer = pdf_service.generate_report(dataset)
            
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating PDF: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def chart_data(self, request, pk=None):
        """Get formatted data for charts"""
        dataset = self.get_object()
        analytics = AnalyticsService()
        chart_data = analytics.prepare_chart_data(dataset)
        return Response(chart_data)
    
    @action(detail=True, methods=['get'])
    def export_excel(self, request, pk=None):
        """Export dataset to Excel format"""
        dataset = self.get_object()
        
        try:
            excel_service = ExcelExportService()
            excel_buffer = excel_service.generate_excel(dataset)
            
            response = HttpResponse(
                excel_buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename=\"dataset_{dataset.id}.xlsx\"'
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating Excel: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail=True, methods=['get'])
    def health_analysis(self, request, pk=None):
        """Get health and efficiency analysis"""
        dataset = self.get_object()
        analytics = AnalyticsService()
        analysis = analytics.analyze_health(dataset)
        return Response(analysis)
    @action(detail=True, methods=['get'])
    def health_analysis(self, request, pk=None):
        """Get health and efficiency analysis"""
        dataset = self.get_object()
        analytics = AnalyticsService()
        analysis = analytics.analyze_health(dataset)
        return Response(analysis)

    @action(detail=False, methods=['post'])
    def root_cause(self, request):
        """Analyze root cause for a specific equipment record/alert"""
        # Parse data { 'pressure': 20, 'temperature': 90 ... }
        # Or simpler: receive alert data directly
        data = request.data
        
        # Mocking a 'Record' object for the service
        class MockRecord:
            def __init__(self, data):
                self.pressure = float(data.get('value', 0) if 'Pressure' in data.get('message', '') else data.get('pressure', 0))
                # If value is string like "20.5" parsing needed. 
                # Let's trust the frontend provides cleaned 'value' or 'pressure' fields
                # Actually, better to receive explicit fields
                self.pressure = float(data.get('pressure', 0))
                self.temperature = float(data.get('temperature', 0))
                self.flowrate = float(data.get('flowrate', 0))
                
        record = MockRecord(data)
        
        analytics = AnalyticsService()
        causes = analytics.analyze_root_cause(record)
        
        return Response({'causes': causes})

    @action(detail=True, methods=['post'])
    def chat(self, request, pk=None):
        """Chat with AI Agent about this dataset"""
        dataset = self.get_object()
        user_message = request.data.get('message', '')
        
        if not user_message:
             return Response({'error': 'Message required'}, status=status.HTTP_400_BAD_REQUEST)
             
        try:
            # Import here to avoid circular dependencies if any, or move to top
            from .services.chat_service import ChatService
            
            chat_service = ChatService()
            ai_response = chat_service.get_response(user_message, dataset)
            
            return Response({'response': ai_response})
        except Exception as e:
            import traceback
            print(traceback.format_exc()) # Log to console for dev
            return Response(
                {'error': f'AI Service Error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
