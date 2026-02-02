from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


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
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout()
        
        # title
        title = QLabel('Chemical Equipment Visualizer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 18px; font-weight: bold; margin: 10px;')
        layout.addWidget(title)
        
        # username field
        layout.addWidget(QLabel('Username:'))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        # password field
        layout.addWidget(QLabel('Password:'))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # login button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        login_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        layout.addWidget(login_btn)
        
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
