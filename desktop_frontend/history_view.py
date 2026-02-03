from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QHBoxLayout, QPushButton, 
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class HistoryView(QWidget):
    """Widget to display upload history"""
    
    def __init__(self, main_window, api_client):
        super().__init__()
        self.main_window = main_window
        self.api_client = api_client
        self.init_ui()
        
    def init_ui(self):
        """Setup UI elements"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_row = QHBoxLayout()
        title = QLabel('Upload History')
        title.setFont(QFont('.AppleSystemUIFont', 24, QFont.Bold))
        title.setStyleSheet('color: #1f2937;')
        header_row.addWidget(title)
        
        # Refresh Button
        refresh_btn = QPushButton('Refresh')
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #667eea;
                border: 1px solid #667eea;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #667eea;
                color: white;
            }
        ''')
        refresh_btn.clicked.connect(self.load_history)
        header_row.addStretch()
        header_row.addWidget(refresh_btn)
        
        layout.addLayout(header_row)
        
        # History Table
        self.table = QTableWidget()
        self.table.setColumnCount(6) # Name, Date, Equip Count, Flowrate, Pressure, Actions
        self.table.setHorizontalHeaderLabels(['Dataset Name', 'Uploaded At', 'Count', 'Avg Flow', 'Avg Pres', 'Actions'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet('''
            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
                padding: 10px;
                gridline-color: transparent;
            }
            QHeaderView::section {
                background-color: transparent;
                color: #6b7280;
                font-weight: bold;
                border: none;
                padding: 10px;
                font-size: 12px;
                text-transform: uppercase;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f3f4f6;
                color: #374151;
            }
            QTableWidget::item:alternate {
                background-color: #f9fafb;
            }
        ''')
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
    def load_history(self):
        """Fetch and display history"""
        try:
            response = self.api_client.get_datasets()
            self.populate_table(response)
        except Exception as e:
            # print(f"Error loading history: {e}") 
            # Silent fail or show simple message
            pass

    def populate_table(self, datasets):
        """Fill table with datasets"""
        self.table.setRowCount(len(datasets))
        
        for i, data in enumerate(datasets):
            # Name
            self.table.setItem(i, 0, QTableWidgetItem(data['filename']))
            
            # Date (Simple formatting)
            uploaded_at = data['uploaded_at'].split('T')[0] 
            self.table.setItem(i, 1, QTableWidgetItem(uploaded_at))
            
            # Stats
            self.table.setItem(i, 2, QTableWidgetItem(str(data['total_equipment'])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{data['avg_flowrate']:.1f}"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{data['avg_pressure']:.1f}"))
            
            # View Button
            view_btn = QPushButton('View Details')
            view_btn.setCursor(Qt.PointingHandCursor)
            view_btn.setStyleSheet('''
                QPushButton {
                    background-color: #10b981;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            ''')
            # Use closure to capture current data
            view_btn.clicked.connect(lambda checked, d=data: self.view_dataset(d))
            
            # Add button to cell
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(view_btn)
            layout.setAlignment(Qt.AlignCenter)
            widget.setLayout(layout)
            self.table.setCellWidget(i, 5, widget)
            
    def view_dataset(self, dataset_full):
        """Switch to dashboard view with this dataset"""
        # We need to fetch full details including records
        try:
            full_data = self.api_client.get_dataset(dataset_full['id'])
            self.main_window.load_dataset_into_dashboard(full_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset details: {str(e)}")
