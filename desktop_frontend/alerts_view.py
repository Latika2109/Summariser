from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QPushButton, QLineEdit, 
                             QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AlertsView(QWidget):
    """Widget to display and manage Equipment Alerts"""
    
    def __init__(self, main_window, api_client):
        super().__init__()
        self.main_window = main_window
        self.api_client = api_client
        self.dataset_id = None
        self.thresholds = {'flowrate': {}, 'pressure': {}, 'temperature': {}}
        self.init_ui()
        
    def init_ui(self):
        """Setup UI elements"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header = QLabel('Equipment Alerts')
        header.setFont(QFont('.AppleSystemUIFont', 24, QFont.Bold))
        header.setStyleSheet('color: #1f2937;')
        main_layout.addWidget(header)
        
        # --- Threshold Settings ---
        settings_group = QFrame()
        settings_group.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
            }
        ''')
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(20, 20, 20, 20)
        
        st_title = QLabel('Set Alert Thresholds')
        st_title.setFont(QFont('.AppleSystemUIFont', 14, QFont.Bold))
        st_title.setStyleSheet('color: #374151; margin-bottom: 10px;')
        settings_layout.addWidget(st_title)
        
        self.threshold_inputs = {}
        
        # Grid for inputs
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Headers
        grid.addWidget(QLabel('Parameter'), 0, 0)
        grid.addWidget(QLabel('Warning'), 0, 1)
        grid.addWidget(QLabel('Critical'), 0, 2)
        grid.addWidget(QLabel('Action'), 0, 3)
        
        params = ['flowrate', 'pressure', 'temperature']
        for i, param in enumerate(params):
            row = i + 1
            lbl = QLabel(param.capitalize())
            lbl.setStyleSheet('font-weight: bold; color: #4b5563;')
            grid.addWidget(lbl, row, 0)
            
            warn_input = QLineEdit()
            warn_input.setPlaceholderText('Warning')
            warn_input.setStyleSheet(self.get_input_style())
            
            crit_input = QLineEdit()
            crit_input.setPlaceholderText('Critical')
            crit_input.setStyleSheet(self.get_input_style())
            
            save_btn = QPushButton('Save')
            save_btn.setCursor(Qt.PointingHandCursor)
            save_btn.setStyleSheet(self.get_btn_style())
            save_btn.clicked.connect(lambda checked, p=param: self.save_threshold(p))
            
            grid.addWidget(warn_input, row, 1)
            grid.addWidget(crit_input, row, 2)
            grid.addWidget(save_btn, row, 3)
            
            self.threshold_inputs[param] = {'warning': warn_input, 'critical': crit_input}
            
        settings_layout.addLayout(grid)
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # --- Summary Cards ---
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(20)
        
        self.stat_cards = {}
        for level in ['Critical', 'Warning', 'Normal']:
            card = QFrame()
            # Style depends on level
            colors = {
                'Critical': ('#fee2e2', '#7f1d1d'),
                'Warning': ('#fef3c7', '#78350f'),
                'Normal': ('#d1fae5', '#064e3b')
            }
            bg, text = colors[level]
            card.setStyleSheet(f'''
                QFrame {{
                    background-color: {bg};
                    border-radius: 12px;
                    border: 1px solid rgba(0,0,0,0.05);
                }}
            ''')
            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(15, 15, 15, 15)
            
            title_lbl = QLabel(level)
            title_lbl.setStyleSheet(f'color: {text}; font-weight: bold;')
            
            count_lbl = QLabel('0')
            count_lbl.setFont(QFont('.AppleSystemUIFont', 24, QFont.Bold))
            count_lbl.setStyleSheet(f'color: {text};')
            
            card_layout.addWidget(title_lbl)
            card_layout.addWidget(count_lbl)
            card.setLayout(card_layout)
            
            summary_layout.addWidget(card)
            self.stat_cards[level] = count_lbl
            
        main_layout.addLayout(summary_layout)
        
        # --- Alerts List ---
        list_label = QLabel('Active Alerts')
        list_label.setFont(QFont('.AppleSystemUIFont', 16, QFont.Bold))
        list_label.setStyleSheet('color: #374151; margin-top: 20px;')
        main_layout.addWidget(list_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.alerts_list_widget = QWidget()
        self.alerts_list_layout = QVBoxLayout()
        self.alerts_list_layout.setSpacing(10)
        self.alerts_list_layout.addStretch() # Push items up
        self.alerts_list_widget.setLayout(self.alerts_list_layout)
        
        scroll.setWidget(self.alerts_list_widget)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
        
        # Initial load of thresholds (global)
        self.load_thresholds()

    def get_input_style(self):
        return '''
             QLineEdit {
                padding: 8px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background: #f9fafb;
            }
            QLineEdit:focus {
                border: 1px solid #667eea;
                background: white;
            }
        '''
        
    def get_btn_style(self):
        return '''
            QPushButton {
                background-color: #4b5563;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #374151;
            }
        '''

    def load_thresholds(self):
        try:
            data = self.api_client.get_thresholds()
            for item in data:
                p = item['parameter']
                if p in self.threshold_inputs:
                    if item['warning_threshold']:
                        self.threshold_inputs[p]['warning'].setText(str(item['warning_threshold']))
                    if item['critical_threshold']:
                        self.threshold_inputs[p]['critical'].setText(str(item['critical_threshold']))
        except Exception as e:
            print(f"Error loading thresholds: {e}")

    def save_threshold(self, parameter):
        warn = self.threshold_inputs[parameter]['warning'].text()
        crit = self.threshold_inputs[parameter]['critical'].text()
        
        try:
            # simple validation
            w_val = float(warn) if warn else None
            c_val = float(crit) if crit else None
            
            self.api_client.set_threshold(parameter, w_val, c_val)
            QMessageBox.information(self, "Success", f"Threshold for {parameter} saved.")
            
            # Refresh if dataset loaded
            if self.dataset_id:
                self.load_alerts(self.dataset_id)
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

    def load_alerts(self, dataset_id):
        self.dataset_id = dataset_id
        if not dataset_id:
            return
            
        try:
            data = self.api_client.get_alerts(dataset_id)
            self.populate_summary(data['summary'])
            self.populate_list(data['alerts'])
        except Exception as e:
            print(f"Error loading alerts: {e}")

    def populate_summary(self, summary):
        self.stat_cards['Critical'].setText(str(summary['critical_alerts']))
        self.stat_cards['Warning'].setText(str(summary['warning_alerts']))
        self.stat_cards['Normal'].setText(str(summary['normal']))

    def populate_list(self, alerts):
        # Clear list (except stretch)
        while self.alerts_list_layout.count() > 1:
            child = self.alerts_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        if not alerts:
            nolabel = QLabel("No active alerts. Equipment is running normally.")
            nolabel.setStyleSheet("color: #6b7280; font-style: italic; margin: 10px;")
            self.alerts_list_layout.insertWidget(0, nolabel)
            return

        for alert in alerts:
            item = QFrame()
            level = alert['level'].capitalize() # warning -> Warning
            colors = {
                'Critical': ('#fee2e2', '#7f1d1d', '#991b1b'), # bg, border, text
                'Warning': ('#fef3c7', '#78350f', '#92400e')
            }
            bg, border, text = colors.get(level, ('#f3f4f6', '#d1d5db', '#374151'))
            
            item.setStyleSheet(f'''
                QFrame {{
                    background-color: {bg};
                    border-left: 5px solid {border};
                    border-radius: 4px;
                }}
            ''')
            
            layout = QHBoxLayout()
            layout.setContentsMargins(15, 15, 15, 15)
            
            info_layout = QVBoxLayout()
            name = QLabel(f"{alert['equipment_name']} - {level}")
            name.setFont(QFont('.AppleSystemUIFont', 13, QFont.Bold))
            name.setStyleSheet(f"color: {text}; border: none;")
            
            msg = QLabel(alert['message'])
            msg.setWordWrap(True)
            msg.setStyleSheet(f"color: {text}; border: none;")
            
            details = QLabel(f"Value: {alert['value']} | Threshold: {alert['threshold']}")
            details.setStyleSheet(f"color: {text}; font-size: 11px; opacity: 0.8; border: none;")
            
            info_layout.addWidget(name)
            info_layout.addWidget(msg)
            info_layout.addWidget(details)
            
            layout.addLayout(info_layout)
            
            # Novel Idea: "Why?" Button (AI Detective)
            why_btn = QPushButton("Analyze Root Cause")
            why_btn.setCursor(Qt.PointingHandCursor)
            why_btn.setFixedWidth(140)
            why_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: white;
                    color: {text};
                    border: 1px solid {text};
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {text};
                    color: white;
                }}
            ''')
            why_btn.clicked.connect(lambda ch, a=alert: self.analyze_root_cause(a))
            
            layout.addWidget(why_btn)
            
            item.setLayout(layout)
            self.alerts_list_layout.insertWidget(self.alerts_list_layout.count()-1, item)

    def analyze_root_cause(self, alert):
        # Construct payload
        params = {
            'pressure': alert['value'] if 'Pressure' in alert['message'] else 0,
            'temperature': alert['value'] if 'Temperature' in alert['message'] else 0,
            'flowrate': alert['value'] if 'Flowrate' in alert['message'] else 0,
        }
        
        try:
            response = self.api_client.get_root_cause(params)
            causes = response['causes']
            
            text = "\n- ".join(causes)
            QMessageBox.information(self, "AI Root Cause Analysis", 
                                    f"Analyzing {alert['equipment_name']}...\n\nPotential Causes:\n- {text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"AI Analysis Failed: {str(e)}")
