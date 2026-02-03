from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class HealthView(QWidget):
    """Widget to display Equipment Health and Efficiency Analysis"""
    
    def __init__(self, main_window, api_client):
        super().__init__()
        self.main_window = main_window
        self.api_client = api_client
        self.dataset_id = None
        self.init_ui()
        
    def init_ui(self):
        """Setup UI elements"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header = QLabel('Health & Efficiency Analytics')
        header.setFont(QFont('.AppleSystemUIFont', 24, QFont.Bold))
        header.setStyleSheet('color: #1f2937;')
        main_layout.addWidget(header)
        
        # Subheader
        sub = QLabel('Real-time condition monitoring')
        sub.setStyleSheet('color: #6b7280; font-size: 14px; margin-bottom: 20px;')
        main_layout.addWidget(sub)
        
        # Content Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_widget = QWidget()
        content_layout = QHBoxLayout() # Split Heatmap vs Efficiency
        content_layout.setSpacing(20)
        
        # --- Left: Heatmap Section ---
        heatmap_card = QFrame()
        heatmap_card.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
            }
        ''')
        heatmap_layout = QVBoxLayout()
        heatmap_layout.setContentsMargins(20, 20, 20, 20)
        
        hm_title = QLabel('Equipment Health Map')
        hm_title.setFont(QFont('.AppleSystemUIFont', 16, QFont.Bold))
        hm_title.setStyleSheet('color: #374151;')
        heatmap_layout.addWidget(hm_title)
        
        # Grid for cells
        self.heatmap_grid = QGridLayout()
        self.heatmap_grid.setSpacing(10)
        heatmap_layout.addLayout(self.heatmap_grid)
        heatmap_layout.addStretch()
        
        heatmap_card.setLayout(heatmap_layout)
        content_layout.addWidget(heatmap_card, 2) # 2/3 width
        
        # --- Right: Efficiency List ---
        eff_card = QFrame()
        eff_card.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
            }
        ''')
        eff_layout = QVBoxLayout()
        eff_layout.setContentsMargins(20, 20, 20, 20)
        
        eff_title = QLabel('Power Intensity Index')
        eff_title.setFont(QFont('.AppleSystemUIFont', 16, QFont.Bold))
        eff_title.setStyleSheet('color: #374151;')
        eff_layout.addWidget(eff_title)
        
        self.eff_table = QTableWidget()
        self.eff_table.setColumnCount(2)
        self.eff_table.setHorizontalHeaderLabels(['Equipment', 'Power (Flow×Pres)'])
        self.eff_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.eff_table.verticalHeader().setVisible(False)
        self.eff_table.setShowGrid(False)
        self.eff_table.setStyleSheet('''
            QTableWidget { border: none; }
            QHeaderView::section {
                background-color: transparent;
                color: #6b7280;
                font-weight: bold;
                border: none;
                text-align: left;
            }
        ''')
        eff_layout.addWidget(self.eff_table)
        
        eff_card.setLayout(eff_layout)
        content_layout.addWidget(eff_card, 1) # 1/3 width
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
        
    def load_data(self, dataset_id):
        self.dataset_id = dataset_id
        if not self.dataset_id:
            return
            
        try:
            data = self.api_client.get_health_analysis(self.dataset_id)
            self.populate_heatmap(data)
            self.populate_efficiency(data)
        except Exception as e:
            print(f"Error loading health data: {e}")

    def populate_heatmap(self, data):
        # Clear existing
        for i in reversed(range(self.heatmap_grid.count())): 
            self.heatmap_grid.itemAt(i).widget().setParent(None)
            
        # Add cells
        row, col = 0, 0
        max_cols = 4
        
        for item in data:
            cell = QFrame()
            
            # Color logic
            bg_color = "#d1fae5" # Green
            text_color = "#064e3b"
            if item['status'] == 'Warning':
                bg_color = "#fef3c7" # Yellow
                text_color = "#78350f"
            elif item['status'] == 'Critical':
                bg_color = "#fee2e2" # Red
                text_color = "#7f1d1d"
                
            cell.setFixedSize(100, 100)
            cell.setStyleSheet(f'''
                background-color: {bg_color};
                border-radius: 12px;
                border: 1px solid rgba(0,0,0,0.05);
            ''')
            
            cell_layout = QVBoxLayout()
            score = QLabel(str(int(item['health_score'])))
            score.setFont(QFont('.AppleSystemUIFont', 20, QFont.Bold))
            score.setAlignment(Qt.AlignCenter)
            score.setStyleSheet(f"color: {text_color}; border: none;")
            
            name = QLabel(item['name'])
            name.setFont(QFont('.AppleSystemUIFont', 10))
            name.setAlignment(Qt.AlignCenter)
            name.setWordWrap(True)
            name.setStyleSheet(f"color: {text_color}; border: none;")
            
            cell_layout.addWidget(score)
            cell_layout.addWidget(name)
            cell.setLayout(cell_layout)
            
            self.heatmap_grid.addWidget(cell, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def populate_efficiency(self, data):
        # Sort by power index desc
        sorted_data = sorted(data, key=lambda x: x['power_index'], reverse=True)[:10]
        
        self.eff_table.setRowCount(len(sorted_data))
        for i, item in enumerate(sorted_data):
            name = QTableWidgetItem(item['name'])
            name.setFont(QFont('.AppleSystemUIFont', 13))
            
            power = QTableWidgetItem(str(int(item['power_index'])))
            power.setFont(QFont('.AppleSystemUIFont', 13, QFont.Bold))
            power.setForeground(QColor('#6366f1'))
            power.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            self.eff_table.setItem(i, 0, name)
            self.eff_table.setItem(i, 1, power)
