
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class ValidationDialog(QDialog):
    """Dialog to show data quality validation"""
    
    def __init__(self, parent=None, api_client=None, dataset_id=None):
        super().__init__(parent)
        self.api_client = api_client
        self.dataset_id = dataset_id
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        self.setWindowTitle('Data Quality Report')
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Card
        card = QFrame()
        card.setStyleSheet('''
            QFrame#MainCard {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
            }
        ''')
        card.setObjectName("MainCard")
        
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel('Data Quality Report')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet('color: #1f2937;')
        subtitle = QLabel('Comprehensive analysis of dataset health')
        subtitle.setStyleSheet('color: #6b7280; font-size: 14px;')
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        
        close_btn = QPushButton('×')
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #9ca3af;
                font-size: 24px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover { color: #4b5563; }
        ''')
        
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        card_layout.addLayout(header_layout)
        
        # Content Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        
        # Loading State
        self.loading_label = QLabel('Analyzing data quality...')
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet('color: #6366f1; font-size: 16px; font-weight: bold; margin-top: 50px;')
        self.content_layout.addWidget(self.loading_label)
        
        scroll.setWidget(self.content_widget)
        card_layout.addWidget(scroll)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        self.setLayout(layout)
        
    def load_data(self):
        try:
            data = self.api_client.validate_dataset(self.dataset_id)
            self.loading_label.hide()
            self.render_report(data)
        except Exception as e:
            self.loading_label.setText(f'Error loading report: {str(e)}')
            self.loading_label.setStyleSheet('color: #ef4444;')
            
    def render_report(self, data):
        # 1. Score Circle
        score = data['quality_score']
        color = '#10b981' if score >= 90 else '#f59e0b' if score >= 70 else '#ef4444'
        
        score_container = QFrame()
        score_layout = QVBoxLayout(score_container)
        score_layout.setAlignment(Qt.AlignCenter)
        
        score_lbl = QLabel(f"{score:.1f}")
        score_lbl.setAlignment(Qt.AlignCenter)
        score_lbl.setStyleSheet(f'''
            font-size: 48px; 
            font-weight: bold; 
            color: {color};
            border: 4px solid {color};
            border-radius: 60px;
            padding: 20px;
            min-width: 120px;
            min-height: 120px;
            background-color: #f9fafb;
        ''')
        score_layout.addWidget(score_lbl)
        
        label = QLabel('QUALITY SCORE')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('color: #6b7280; font-weight: bold; margin-top: 10px; letter-spacing: 1px;')
        score_layout.addWidget(label)
        
        self.content_layout.addWidget(score_container)
        
        # 2. Metrics Grid
        metrics_frame = QFrame()
        metrics_layout = QHBoxLayout(metrics_frame)
        metrics_layout.setSpacing(15)
        
        self.add_metric_card(metrics_layout, 'Total Records', data['total_records'], '#3b82f6')
        self.add_metric_card(metrics_layout, 'Missing Values', data['missing_values'], '#f59e0b')
        self.add_metric_card(metrics_layout, 'Duplicates', data['duplicate_records'], '#8b5cf6')
        self.add_metric_card(metrics_layout, 'Outliers', data['outliers_count'], '#ef4444')
        
        self.content_layout.addWidget(metrics_frame)
        
        # 3. Outliers Details (if any)
        if data['outliers_count'] > 0:
            outlier_group = QFrame()
            outlier_group.setStyleSheet('.QFrame { background: #fee2e2; border-radius: 10px; padding: 15px; }')
            outlier_layout = QVBoxLayout(outlier_group)
            
            title = QLabel('Outlier Analysis')
            title.setStyleSheet('color: #b91c1c; font-weight: bold; font-size: 14px;')
            outlier_layout.addWidget(title)
            
            for item in data['details']['outliers']:
                det = QLabel(f"• {item['parameter'].title()}: {item['count']} outliers (Range: {item['lower_bound']:.2f} - {item['upper_bound']:.2f})")
                det.setStyleSheet('color: #7f1d1d; margin-top: 5px;')
                outlier_layout.addWidget(det)
                
            self.content_layout.addWidget(outlier_group)
            
        self.content_layout.addStretch()

    def add_metric_card(self, layout, title, value, color):
        frame = QFrame()
        frame.setStyleSheet('''
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
                border: 1px solid #f3f4f6;
            }
        ''')
        fl = QVBoxLayout(frame)
        
        t = QLabel(title.upper())
        t.setStyleSheet('color: #9ca3af; font-size: 11px; font-weight: bold;')
        fl.addWidget(t)
        
        v = QLabel(str(value))
        v.setStyleSheet(f'color: {color}; font-size: 24px; font-weight: bold;')
        fl.addWidget(v)
        
        layout.addWidget(frame)
