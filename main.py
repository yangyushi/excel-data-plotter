import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
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
        
        self.line_plot_button = QRadioButton("Line Plot", self)
        self.line_plot_button.setChecked(True)
        self.scatter_plot_button = QRadioButton("Scatter Plot", self)
        
        self.x_combo = QComboBox(self)
        self.x_combo.setEnabled(False)
        self.y_combo = QComboBox(self)
        self.y_combo.setEnabled(False)
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('X-axis:'))
        hbox.addWidget(self.x_combo)
        hbox.addWidget(QLabel('Y-axis:'))
        hbox.addWidget(self.y_combo)
        hbox.addStretch(1)
        hbox.addWidget(self.line_plot_button)
        hbox.addWidget(self.scatter_plot_button)
        hbox.addWidget(self.load_button)
        hbox.addWidget(self.plot_button)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)
        
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
            self.plot_button.setEnabled(True)
    
    def plot_data(self):
        x = self.x_combo.currentText()
        y = self.y_combo.currentText()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if self.line_plot_button.isChecked():
            ax.plot(self.df[x], self.df[y])
        else:
            ax.scatter(self.df[x], self.df[y])
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())

