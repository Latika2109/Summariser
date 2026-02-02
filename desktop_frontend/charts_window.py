import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDialog, QVBoxLayout


class ChartWindow(QDialog):
    """Popup window to display matplotlib charts"""
    
    def __init__(self, title, chart_type, data):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == 'type_distribution':
            self.create_type_chart(ax, data)
        elif chart_type == 'temperature':
            self.create_temperature_chart(ax, data)
        elif chart_type == 'pressure':
            self.create_pressure_chart(ax, data)
        
        # embed in Qt
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        self.setLayout(layout)
    
    def create_type_chart(self, ax, type_distribution):
        """Create bar chart for equipment type distribution"""
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        
        ax.bar(types, counts, color='steelblue')
        ax.set_xlabel('Equipment Type')
        ax.set_ylabel('Count')
        ax.set_title('Equipment Type Distribution')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.tight_layout()
    
    def create_temperature_chart(self, ax, records):
        """Create line chart for temperature data"""
        names = [r['equipment_name'] for r in records]
        temps = [r['temperature'] for r in records]
        
        ax.plot(range(len(names)), temps, marker='o', color='red', linewidth=2)
        ax.set_xlabel('Equipment Index')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Temperature by Equipment')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
    
    def create_pressure_chart(self, ax, records):
        """Create line chart for pressure data"""
        names = [r['equipment_name'] for r in records]
        pressures = [r['pressure'] for r in records]
        
        ax.plot(range(len(names)), pressures, marker='s', color='green', linewidth=2)
        ax.set_xlabel('Equipment Index')
        ax.set_ylabel('Pressure (bar)')
        ax.set_title('Pressure by Equipment')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
