from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QFileDialog, QMessageBox, QLabel, QGroupBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from charts_window import ChartWindow


class UploadWindow(QMainWindow):
    """Main window with upload, table view, and chart buttons"""
    
    def __init__(self, api_client, user_data):
        super().__init__()
        self.api_client = api_client
        self.user_data = user_data
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Setup UI elements"""
        self.setWindowTitle('Equipment Data Visualizer')
        self.setGeometry(100, 100, 1100, 750)
        
        # set window style
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f5f7fa;
            }
        ''')
        
        # main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # header with gradient
        header_frame = QFrame()
        header_frame.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 20px;
            }
        ''')
        header_layout = QVBoxLayout()
        
        header_title = QLabel('🔬 Chemical Equipment Visualizer')
        header_title.setStyleSheet('color: white; font-size: 24px; font-weight: bold;')
        header_layout.addWidget(header_title)
        
        header_user = QLabel(f'Welcome, {self.user_data["username"]}')
        header_user.setStyleSheet('color: rgba(255, 255, 255, 0.9); font-size: 14px;')
        header_layout.addWidget(header_user)
        
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # upload section
        upload_group = QGroupBox('📁 Upload CSV File')
        upload_group.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        ''')
        upload_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton('📤 Select and Upload CSV')
        self.upload_btn.clicked.connect(self.handle_upload)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #653a8b);
            }
            QPushButton:pressed {
                padding-top: 14px;
                padding-bottom: 10px;
            }
        ''')
        upload_layout.addWidget(self.upload_btn)
        upload_layout.addStretch()
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # summary stats
        self.stats_label = QLabel('📊 No data loaded yet')
        self.stats_label.setStyleSheet('''
            QLabel {
                padding: 20px;
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
            }
        ''')
        layout.addWidget(self.stats_label)
        
        # chart buttons
        chart_group = QGroupBox('📈 Visualizations')
        chart_group.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        ''')
        chart_layout = QHBoxLayout()
        
        self.type_chart_btn = QPushButton('📊 Type Distribution')
        self.type_chart_btn.clicked.connect(lambda: self.show_chart('type_distribution'))
        self.type_chart_btn.setEnabled(False)
        self.type_chart_btn.setCursor(Qt.PointingHandCursor)
        self.type_chart_btn.setStyleSheet('''
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
                color: #9ca3af;
            }
        ''')
        chart_layout.addWidget(self.type_chart_btn)
        
        self.temp_chart_btn = QPushButton('🌡️ Temperature')
        self.temp_chart_btn.clicked.connect(lambda: self.show_chart('temperature'))
        self.temp_chart_btn.setEnabled(False)
        self.temp_chart_btn.setCursor(Qt.PointingHandCursor)
        self.temp_chart_btn.setStyleSheet('''
            QPushButton {
                background-color: #f59e0b;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #d97706;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
                color: #9ca3af;
            }
        ''')
        chart_layout.addWidget(self.temp_chart_btn)
        
        self.pressure_chart_btn = QPushButton('💨 Pressure')
        self.pressure_chart_btn.clicked.connect(lambda: self.show_chart('pressure'))
        self.pressure_chart_btn.setEnabled(False)
        self.pressure_chart_btn.setCursor(Qt.PointingHandCursor)
        self.pressure_chart_btn.setStyleSheet('''
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #2563eb;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
                color: #9ca3af;
            }
        ''')
        chart_layout.addWidget(self.pressure_chart_btn)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        # data table
        table_label = QLabel('📋 Equipment Data')
        table_label.setStyleSheet('font-weight: bold; font-size: 14px; margin-top: 10px;')
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet('''
            QTableWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:alternate {
                background-color: #f9fafb;
            }
        ''')
        layout.addWidget(self.table)
        
        main_widget.setLayout(layout)
    
    def handle_upload(self):
        """Handle CSV file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Select CSV File', 
            '', 
            'CSV Files (*.csv)'
        )
        
        if not file_path:
            return
        
        try:
            # upload file
            response = self.api_client.upload_csv(file_path)
            self.current_dataset = response
            
            # update UI
            self.update_stats()
            self.populate_table()
            
            # enable chart buttons
            self.type_chart_btn.setEnabled(True)
            self.temp_chart_btn.setEnabled(True)
            self.pressure_chart_btn.setEnabled(True)
            
            QMessageBox.information(self, 'Success', '✅ CSV uploaded successfully!')
            
        except Exception as e:
            QMessageBox.critical(self, 'Upload Failed', f'❌ Error: {str(e)}')
    
    def update_stats(self):
        """Update summary statistics display"""
        if not self.current_dataset:
            return
        
        stats_text = f"""
        <div style='line-height: 1.6;'>
        <b style='font-size: 15px; color: #667eea;'>📊 Dataset Summary</b><br><br>
        <b>Total Equipment:</b> {self.current_dataset['total_equipment']}<br>
        <b>Avg Flowrate:</b> {self.current_dataset['avg_flowrate']:.2f}<br>
        <b>Avg Pressure:</b> {self.current_dataset['avg_pressure']:.2f}<br>
        <b>Avg Temperature:</b> {self.current_dataset['avg_temperature']:.2f}
        </div>
        """
        self.stats_label.setText(stats_text)
    
    def populate_table(self):
        """Fill table with equipment records"""
        if not self.current_dataset or 'records' not in self.current_dataset:
            return
        
        records = self.current_dataset['records']
        self.table.setRowCount(len(records))
        
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(record['equipment_name']))
            self.table.setItem(i, 1, QTableWidgetItem(record['equipment_type']))
            self.table.setItem(i, 2, QTableWidgetItem(str(record['flowrate'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(record['pressure'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(record['temperature'])))
    
    def show_chart(self, chart_type):
        """Open chart window"""
        if not self.current_dataset:
            QMessageBox.warning(self, 'No Data', 'Please upload a CSV file first')
            return
        
        if chart_type == 'type_distribution':
            chart = ChartWindow(
                'Equipment Type Distribution',
                'type_distribution',
                self.current_dataset['type_distribution']
            )
        elif chart_type == 'temperature':
            chart = ChartWindow(
                'Temperature Data',
                'temperature',
                self.current_dataset['records']
            )
        elif chart_type == 'pressure':
            chart = ChartWindow(
                'Pressure Data',
                'pressure',
                self.current_dataset['records']
            )
        
        chart.exec_()
