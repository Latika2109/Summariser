from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
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
        self.setFixedSize(450, 350)
        
        # set window background
        self.setStyleSheet('''
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        ''')
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # create white card container
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 30px;
            }
        ''')
        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)
        
        # title
        title = QLabel('🔬 Equipment Visualizer')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet('color: #333; margin-bottom: 10px;')
        card_layout.addWidget(title)
        
        # subtitle
        subtitle = QLabel('Desktop Application')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('color: #666; font-size: 13px; margin-bottom: 20px;')
        card_layout.addWidget(subtitle)
        
        # username field
        username_label = QLabel('Username')
        username_label.setStyleSheet('color: #333; font-weight: bold; font-size: 13px;')
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet('''
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        ''')
        card_layout.addWidget(self.username_input)
        
        # password field
        password_label = QLabel('Password')
        password_label.setStyleSheet('color: #333; font-weight: bold; font-size: 13px;')
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet('''
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        ''')
        card_layout.addWidget(self.password_input)
        
        # login button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 14px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #653a8b);
            }
            QPushButton:pressed {
                padding-top: 16px;
                padding-bottom: 12px;
            }
        ''')
        card_layout.addWidget(login_btn)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        
        self.setLayout(layout)
    
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
