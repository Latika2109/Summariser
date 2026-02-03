
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from equipment_api.models import EquipmentDataset
from equipment_api.services.validation_service import ValidationService
from equipment_api.services.email_service import EmailService
from equipment_api.services.pdf_service import PDFService

def debug_services():
    print("--- Starting Debug ---")
    
    # Get a dataset
    dataset = EquipmentDataset.objects.last()
    if not dataset:
        print("No datasets found to test with.")
        return

    print(f"Testing with dataset: {dataset.filename} (ID: {dataset.id})")
    
    # 1. Test Validation
    print("\n[1] Testing ValidationService...")
    try:
        report = ValidationService.validate_dataset(dataset)
        print(f"Validation successful. Score: {report.quality_score}")
    except Exception as e:
        print(f"VALIDATION ERROR: {e}")
        import traceback
        traceback.print_exc()

    # 2. Test PDF Generation (internal part of Email)
    print("\n[2] Testing PDF Generation...")
    try:
        service = PDFService()
        pdf_buffer = service.generate_report(dataset)
        print(f"PDF generation successful. Size: {len(pdf_buffer.getvalue())} bytes")
    except Exception as e:
        print(f"PDF ERROR: {e}")
        import traceback
        traceback.print_exc()

    # 3. Test Email
    print("\n[3] Testing Email Sending...")
    try:
        # Send to the user's email if possible, or a test one
        email = "dataset_owner@example.com"
        print(f"Attempting to send email to {email}...")
        
        success, message = EmailService.send_report_email(dataset, email)
        
        if success:
            print(f"Email sent successfully: {message}")
        else:
            print(f"Email failed (logic): {message}")
            
    except Exception as e:
        print(f"EMAIL CRASH: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_services()
