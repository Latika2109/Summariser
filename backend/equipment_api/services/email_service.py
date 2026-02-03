"""Email service for sending reports and notifications"""
from django.core.mail import EmailMessage
from django.conf import settings
from equipment_api.services.pdf_service import PDFService
import io


class EmailService:
    """Handle email notifications and scheduled reports"""
    
    @staticmethod
    def send_report_email(dataset, user_email, include_charts=True, include_alerts=True):
        """Send dataset report via email"""
        
        # Generate PDF report
        pdf_buffer = PDFService().generate_report(dataset)
        
        # Create email
        subject = f'Equipment Data Report - {dataset.filename}'
        
        body = f"""
        Dear User,
        
        Please find attached the equipment data report for {dataset.filename}.
        
        Summary:
        - Total Equipment: {dataset.total_equipment}
        - Average Flowrate: {dataset.avg_flowrate:.2f}
        - Average Pressure: {dataset.avg_pressure:.2f}
        - Average Temperature: {dataset.avg_temperature:.2f}
        
        Upload Date: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}
        
        Best regards,
        Chemical Equipment Visualizer System
        """
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        
        # Attach PDF
        email.attach(
            f'{dataset.filename}_report.pdf',
            pdf_buffer.getvalue(),
            'application/pdf'
        )
        
        # Send email
        try:
            email.send()
            return True, "Email sent successfully"
        except Exception as e:
            print(f"Error sending email: {e}")
            return False, str(e)
    
    @staticmethod
    def send_alert_email(user_email, alerts):
        """Send alert notification email"""
        
        subject = f'Equipment Alerts - {len(alerts)} items require attention'
        
        alert_list = '\n'.join([
            f"- {alert['equipment_name']}: {alert['message']}"
            for alert in alerts
        ])
        
        body = f"""
        Dear User,
        
        The following equipment items have triggered alerts:
        
        {alert_list}
        
        Please review these items in the Chemical Equipment Visualizer application.
        
        Best regards,
        Chemical Equipment Visualizer System
        """
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        
        try:
            email.send()
            return True
        except Exception as e:
            print(f"Error sending alert email: {e}")
            return False
