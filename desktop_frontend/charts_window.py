import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QLinearGradient, QColor


class ChartWindow(QDialog):
    """Popup window to display matplotlib charts"""
    
    def __init__(self, title, chart_type, data):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 900, 700)
        
        # Set window styling
        self.setWindowFlags(Qt.FramelessWindowHint)  # Modern frameless window
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Background Frame
        self.frame = QFrame()
        self.frame.setStyleSheet('''
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        ''')
        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet('color: #1f2937;')
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        close_btn = QPushButton('×')
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #6b7280;
                font-size: 24px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ef4444;
            }
        ''')
        header_layout.addWidget(close_btn)
        layout.addLayout(header_layout)
        
        # Chart configuration
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#f9fafb')
        
        if chart_type == 'type_distribution':
            self.create_type_chart(ax, data)
        elif chart_type == 'temperature':
            self.create_temperature_chart(ax, data)
        elif chart_type == 'pressure':
            self.create_pressure_chart(ax, data)
        
        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
        ax.tick_params(colors='#6b7280')

        # Embed in Qt
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet('background-color: transparent;')
        layout.addWidget(canvas)
        
        main_layout.addWidget(self.frame)
        self.setLayout(main_layout)
        
        # Enable dragging
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
    
    def create_type_chart(self, ax, type_distribution):
        """Create bar chart for equipment type distribution"""
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        
        bars = ax.bar(types, counts, color='#667eea', width=0.6)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', color='#4b5563', fontweight='bold')
            
        ax.set_xlabel('Equipment Type', color='#374151', fontweight='bold', labelpad=10)
        ax.set_ylabel('Count', color='#374151', fontweight='bold', labelpad=10)
        ax.set_title('Equipment Type Distribution', color='#111827', fontsize=14, fontweight='bold', pad=20)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.tight_layout()
    
    def create_temperature_chart(self, ax, records):
        """Create line chart for temperature data"""
        names = [r['equipment_name'] for r in records]
        temps = [r['temperature'] for r in records]
        
        # Gradient fill
        ax.fill_between(range(len(names)), temps, alpha=0.1, color='#ef4444')
        ax.plot(range(len(names)), temps, marker='o', color='#ef4444', linewidth=2, markersize=6)
        
        ax.set_xlabel('Equipment Index', color='#374151', fontweight='bold', labelpad=10)
        ax.set_ylabel('Temperature (°C)', color='#374151', fontweight='bold', labelpad=10)
        ax.set_title('Temperature by Equipment', color='#111827', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
    
    def create_pressure_chart(self, ax, records):
        """Create line chart for pressure data"""
        names = [r['equipment_name'] for r in records]
        pressures = [r['pressure'] for r in records]
        
        # Gradient fill
        ax.fill_between(range(len(names)), pressures, alpha=0.1, color='#10b981')
        ax.plot(range(len(names)), pressures, marker='s', color='#10b981', linewidth=2, markersize=6)
        
        ax.set_xlabel('Equipment Index', color='#374151', fontweight='bold', labelpad=10)
        ax.set_ylabel('Pressure (bar)', color='#374151', fontweight='bold', labelpad=10)
        ax.set_title('Pressure by Equipment', color='#111827', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
