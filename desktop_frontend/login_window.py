from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor


class LoginWindow(QDialog):
    """Login dialog for user authentication"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.user_data = None
        self.init_ui()
    
    def init_ui(self):
        """Setup UI elements"""
        self.setWindowTitle('Login - Equipment Visualizer')
        self.setFixedSize(450, 480)
        
        # Modern Frameless Window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main White Card
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background-color: #ffffff;
                border-radius: 20px;
                border: 1px solid #e5e7eb;
            }
        ''')
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 30, 40, 40)
        card_layout.setSpacing(10)
        
        # Close Button (Top Right)
        close_btn = QPushButton('×')
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #9ca3af;
                border-radius: 15px;
                font-size: 24px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: #f3f4f6;
                color: #6b7280;
            }
        ''')
        
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        card_layout.addLayout(header_layout)
        
        # Logo/Title Section
        title = QLabel('Chemical\nVisualizer')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('.AppleSystemUIFont', 24, QFont.Bold))
        title.setStyleSheet('color: #1f2937; margin-bottom: 5px;')
        card_layout.addWidget(title)
        
        subtitle = QLabel('Desktop Application')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('color: #6b7280; font-size: 14px; margin-bottom: 30px;')
        card_layout.addWidget(subtitle)
        
        # Form Container
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.username_input.setStyleSheet('''
            QLineEdit {
                padding: 15px;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                font-size: 14px;
                background-color: #f9fafb;
                color: #1f2937;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                border: 1px solid #667eea;
            }
        ''')
        form_layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet('''
            QLineEdit {
                padding: 15px;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                font-size: 14px;
                background-color: #f9fafb;
                color: #1f2937;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                border: 1px solid #667eea;
            }
        ''')
        form_layout.addWidget(self.password_input)
        
        form_widget.setLayout(form_layout)
        card_layout.addWidget(form_widget)
        
        # Login Button
        login_btn = QPushButton('Sign In')
        login_btn.clicked.connect(self.handle_login)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 15px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5b6ede, stop:1 #674291);
            }
            QPushButton:pressed {
                padding-top: 17px;
                padding-bottom: 13px;
            }
        ''')
        card_layout.addWidget(login_btn)
        
        card_layout.addStretch()
        card.setLayout(card_layout)
        layout.addWidget(card)
        
        self.setLayout(layout)
        
        # Dragging logic
        self.old_pos = None

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            # call API
            response = self.api_client.login(username, password)
            self.api_client.set_token(response['token'])
            self.user_data = response['user']
            
            # close dialog and accept
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, 'Login Failed', f'Error: {str(e)}')
