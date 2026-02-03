
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

try:
    print("Testing imports...")
    import pandas as pd
    print("Pandas imported successfully")
    import reportlab
    from reportlab.pdfgen import canvas
    print("Reportlab imported successfully")
    
    from equipment_api.services.validation_service import ValidationService
    from equipment_api.services.email_service import EmailService
    print("Services imported successfully")
    
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)

print("All import checks passed.")
