from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QFileDialog, QMessageBox, QLabel, QGroupBox)
from PyQt5.QtCore import Qt
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
        self.setGeometry(100, 100, 1000, 700)
        
        # main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # header
        header = QLabel(f'Welcome, {self.user_data["username"]}')
        header.setStyleSheet('font-size: 16px; font-weight: bold; padding: 10px;')
        layout.addWidget(header)
        
        # upload section
        upload_group = QGroupBox('Upload CSV File')
        upload_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton('Select and Upload CSV')
        self.upload_btn.clicked.connect(self.handle_upload)
        self.upload_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        upload_layout.addWidget(self.upload_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # summary stats
        self.stats_label = QLabel('No data loaded')
        self.stats_label.setStyleSheet('padding: 10px; background: #f0f0f0; border-radius: 5px;')
        layout.addWidget(self.stats_label)
        
        # chart buttons
        chart_group = QGroupBox('Visualizations')
        chart_layout = QHBoxLayout()
        
        self.type_chart_btn = QPushButton('Type Distribution Chart')
        self.type_chart_btn.clicked.connect(lambda: self.show_chart('type_distribution'))
        self.type_chart_btn.setEnabled(False)
        chart_layout.addWidget(self.type_chart_btn)
        
        self.temp_chart_btn = QPushButton('Temperature Chart')
        self.temp_chart_btn.clicked.connect(lambda: self.show_chart('temperature'))
        self.temp_chart_btn.setEnabled(False)
        chart_layout.addWidget(self.temp_chart_btn)
        
        self.pressure_chart_btn = QPushButton('Pressure Chart')
        self.pressure_chart_btn.clicked.connect(lambda: self.show_chart('pressure'))
        self.pressure_chart_btn.setEnabled(False)
        chart_layout.addWidget(self.pressure_chart_btn)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        # data table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.table.horizontalHeader().setStretchLastSection(True)
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
            
            QMessageBox.information(self, 'Success', 'CSV uploaded successfully!')
            
        except Exception as e:
            QMessageBox.critical(self, 'Upload Failed', f'Error: {str(e)}')
    
    def update_stats(self):
        """Update summary statistics display"""
        if not self.current_dataset:
            return
        
        stats_text = f"""
        <b>Dataset Summary:</b><br>
        Total Equipment: {self.current_dataset['total_equipment']}<br>
        Avg Flowrate: {self.current_dataset['avg_flowrate']:.2f}<br>
        Avg Pressure: {self.current_dataset['avg_pressure']:.2f}<br>
        Avg Temperature: {self.current_dataset['avg_temperature']:.2f}
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
