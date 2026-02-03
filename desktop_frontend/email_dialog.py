
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class EmailDialog(QDialog):
    """Dialog to send email report"""
    
    def __init__(self, parent=None, api_client=None, dataset_id=None):
        super().__init__(parent)
        self.api_client = api_client
        self.dataset_id = dataset_id
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Send Email Report')
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Card
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
            }
        ''')
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel('Email Report')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setStyleSheet('color: #1f2937;')
        subtitle = QLabel('Send summary and charts to your team')
        subtitle.setStyleSheet('color: #6b7280; font-size: 13px;')
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        card_layout.addLayout(header_layout)
        
        # Input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter email address')
        self.email_input.setStyleSheet('''
            QLineEdit {
                padding: 12px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background: #f9fafb;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #6366f1;
                background: white;
            }
        ''')
        card_layout.addWidget(self.email_input)
        
        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        self.send_btn = QPushButton('Send Report')
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.clicked.connect(self.send_email)
        self.send_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #8b5cf6);
                color: white;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
            }
        ''')
        
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.close)
        self.cancel_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #6b7280;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
            QPushButton:hover {
                color: #374151;
            }
        ''')
        
        btn_layout.addWidget(self.send_btn)
        btn_layout.addWidget(self.cancel_btn)
        card_layout.addLayout(btn_layout)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        self.setLayout(layout)
        
    def send_email(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, 'Input Error', 'Please enter an email address')
            return
            
        self.send_btn.setText('Sending...')
        self.send_btn.setEnabled(False)
        
        try:
            response = self.api_client.send_report_email(self.dataset_id, email)
            if response.get('success'):
                QMessageBox.information(self, 'Success', 'Email sent successfully!')
                self.close()
            else:
                error_msg = response.get('error', 'Unknown error')
                QMessageBox.critical(self, 'Failed', f'Failed to send email:\n{error_msg}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Network Error: {str(e)}')
        
        self.send_btn.setText('Send Report')
        self.send_btn.setEnabled(True)
