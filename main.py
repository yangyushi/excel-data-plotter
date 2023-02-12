import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Data Plotter')
        self.setGeometry(100, 100, 800, 600)
        
        self.load_button = QPushButton('Load', self)
        self.load_button.clicked.connect(self.load_data)
        
        self.plot_button = QPushButton('Plot', self)
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_button.setEnabled(False)
        
        self.x_combo = QComboBox(self)
        self.x_combo.setEnabled(False)
        self.y_combo = QComboBox(self)
        self.y_combo.setEnabled(False)
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('X-axis:'))
        hbox.addWidget(self.x_combo)
        hbox.addWidget(QLabel('Y-axis:'))
        hbox.addWidget(self.y_combo)
        hbox.addStretch(1)
        hbox.addWidget(self.load_button)
        hbox.addWidget(self.plot_button)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        
        central_widget = QWidget(self)
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
        
    def load_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            self.df = pd.read_excel(file_name)
            self.x_combo.clear()
            self.y_combo.clear()
            self.x_combo.addItems(list(self.df.columns))
            self.y_combo.addItems(list(self.df.columns))
            self.x_combo.setEnabled(True)
            self.y_combo.setEnabled(True)
            self
