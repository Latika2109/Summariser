from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QScrollArea, QFrame, 
                             QGraphicsDropShadowEffect, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class ChatWidget(QWidget):
    """Floating AI Assistant Widget"""
    
    navigate_signal = pyqtSignal(str) # Signal to request navigation
    
    def __init__(self, parent=None, api_client=None):
        super().__init__(parent)
        self.api_client = api_client
        self.dataset_id = None
        self.is_open = False
        self.messages = [{'role': 'ai', 'text': 'Hi! I am your Equipment Assistant. Ask me anything.'}]
        
        self.init_ui()
        
    def init_ui(self):
        # We need to be on top of everything
        # In a real app we might use a separate Window, but a child widget with raise_() works for "floating" feel inside the main window
        self.setFixedSize(350, 500)
        
        # Transparent background for the widget itself, so we can have rounded corners on the frame
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Frame
        self.frame = QFrame()
        self.frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 15px;
            }
        ''')
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 5)
        self.frame.setGraphicsEffect(shadow)
        
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2);
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border-bottom: none;
            }
        ''')
        header.setFixedHeight(50)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        title = QLabel("AI Assistant")
        title.setFont(QFont('.AppleSystemUIFont', 14, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.toggle_chat)
        close_btn.setStyleSheet('''
            QPushButton {
                color: white; 
                background: transparent; 
                font-size: 20px; 
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { color: #fee2e2; }
        ''')
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        header.setLayout(header_layout)
        frame_layout.addWidget(header)
        
        # Messages Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background: #f9fafb;")
        
        self.msg_container = QWidget()
        self.msg_container.setStyleSheet("background: transparent;")
        self.msg_layout = QVBoxLayout()
        self.msg_layout.setSpacing(10)
        self.msg_layout.addStretch()
        self.msg_container.setLayout(self.msg_layout)
        
        self.scroll.setWidget(self.msg_container)
        frame_layout.addWidget(self.scroll)
        
        # Input Area
        input_area = QFrame()
        input_area.setStyleSheet("background: white; border-top: 1px solid #e5e7eb; border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;")
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a question...")
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet('''
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 18px;
                padding: 8px 12px;
                background: white;
            }
            QLineEdit:focus { border: 1px solid #667eea; }
        ''')
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                border-radius: 18px;
                padding: 8px 15px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { background-color: #5b6ede; }
        ''')
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        input_area.setLayout(input_layout)
        frame_layout.addWidget(input_area)
        
        self.frame.setLayout(frame_layout)
        layout.addWidget(self.frame)
        self.setLayout(layout)
        
        self.render_messages()
        self.hide() # Start hidden
        
    def render_messages(self):
        # Clear existing (except stretch)
        while self.msg_layout.count() > 1:
            child = self.msg_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        for msg in self.messages:
            self.add_message_bubble(msg['text'], msg['role'])
            
    def add_message_bubble(self, text, role):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setFont(QFont('.AppleSystemUIFont', 12))
        bubble.setContentsMargins(12, 8, 12, 8)
        
        if role == 'user':
            bubble.setStyleSheet('''
                background-color: #667eea;
                color: white;
                border-radius: 12px;
                border-bottom-right-radius: 2px;
                padding: 10px;
            ''')
            align = Qt.AlignRight
        else:
            bubble.setStyleSheet('''
                background-color: white;
                color: #374151;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                border-bottom-left-radius: 2px;
                padding: 10px;
            ''')
            align = Qt.AlignLeft
            
        wrapper = QHBoxLayout()
        if role == 'user':
            wrapper.addStretch()
            wrapper.addWidget(bubble)
        else:
            wrapper.addWidget(bubble)
            wrapper.addStretch()
            
        self.msg_layout.insertLayout(self.msg_layout.count()-1, wrapper)
        
        # Scroll to bottom
        QTimer.singleShot(100, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        ))

    def send_message(self):
        text = self.input_field.text().strip()
        if not text: return
        
        if not self.dataset_id:
            self.messages.append({'role': 'ai', 'text': 'Please load a dataset first.'})
            self.render_messages()
            self.input_field.clear()
            return

        # Add user message
        self.messages.append({'role': 'user', 'text': text})
        self.add_message_bubble(text, 'user')
        self.input_field.clear()
        self.input_field.setDisabled(True)
        
        # Add thinking placeholder? (Skip for simplicity, just lock input)
        
        # Async call would be better but keeping simple with sync requests for now (threaded ideally)
        # Using a QTimer to allow UI update before blocking call, or better, use a thread.
        # For this prototype, we'll block briefly or use a simplistic approach.
        QTimer.singleShot(100, lambda: self._fetch_response(text))

    def _fetch_response(self, text):
        try:
            response = self.api_client.send_chat_message(self.dataset_id, text)
            raw_reply = response['response']
            
            # Parse Nav
            clean_reply = raw_reply
            if '<<NAV:' in raw_reply:
                import re
                match = re.search(r'<<NAV:([A-Z]+)>>', raw_reply)
                if match:
                    dest = match.group(1)
                    clean_reply = raw_reply.replace(match.group(0), '').strip()
                    self.navigate_signal.emit(dest)
            
            self.messages.append({'role': 'ai', 'text': clean_reply})
            self.add_message_bubble(clean_reply, 'ai')
            
        except Exception as e:
            err = "Sorry, connection error."
            self.messages.append({'role': 'ai', 'text': err})
            self.add_message_bubble(err, 'ai')
            print(e)
            
        self.input_field.setDisabled(False)
        self.input_field.setFocus()

    def toggle_chat(self):
        if self.isHidden():
            self.show()
            self.raise_()
        else:
            self.hide()

    def set_dataset(self, dataset_id):
        self.dataset_id = dataset_id
