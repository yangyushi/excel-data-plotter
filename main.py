import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QLineEdit, QWidget
from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Model(QObject):
    data_loaded = pyqtSignal(pd.DataFrame)
    
    def __init__(self):
        super().__init__()
        self.df = None
    
    def load_data(self, file_name):
        self.df = pd.read_excel(file_name)
        self.data_loaded.emit(self.df)
    
    def get_data(self):
        return self.df
    
class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Data Plotter')
        self.setGeometry(100, 100, 800, 600)
        
        self.load_button = QPushButton('Load', self)
        self.plot_button = QPushButton('Plot', self)
        self.plot_button.setEnabled(False)
        
        self.line_plot_button = QRadioButton("Line Plot", self)
        self.line_plot_button.setChecked(True)
        self.scatter_plot_button = QRadioButton("Scatter Plot", self)
        
        self.x_combo = QComboBox(self)
        self.x_combo.setEnabled(False)
        self.y_combo = QComboBox(self)
        self.y_combo.setEnabled(False)
        
        self.y_transform_edit = QLineEdit(self)
        self.y_transform_edit.setEnabled(False)
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('X-axis:'))
        hbox.addWidget(self.x_combo)
        hbox.addWidget(QLabel('Y-axis:'))
        hbox.addWidget(self.y_combo)
        hbox.addWidget(QLabel('Y-Transformation:'))
        hbox.addWidget(self.y_transform_edit)
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

class Controller(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.view.load_button.clicked.connect(self.load_data)
        self.view.plot_button.clicked.connect(self.plot_data)
        self.model.data_loaded.connect(self.data_loaded)
        
    def load_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Load Data", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            self.model.load_data(file_name)
    
    def data_loaded(self, df):
        self.view.x_combo.clear()
        self.view.y_combo.clear()
        self.view.x_combo.addItems(list(df.columns))
        self.view.y_combo.addItems(list(df.columns))
        self.view.x_combo.setEnabled(True)
        self.view.y_combo.setEnabled(True)
        self.view.y_transform_edit.setEnabled(True)
        self.view.plot_button.setEnabled(True)
    
    def plot_data(self):
        x = self.view.x_combo.currentText()
        y = self.view.y_combo.currentText()
        y_transform = self.view.y_transform_edit.text()
        df = self.model.get_data()
        if y_transform:
            try:
                y_transform = eval(f"lambda y: {y_transform}")
                y_data = y_transform(df[y])
            except:
                y_data = df[y]
        else:
            y_data = df[y]
        self.view.figure.clear()
        ax = self.view.figure.add_subplot(111)
        if self.view.line_plot_button.isChecked():
            ax.plot(df[x], y_data)
        else:
            ax.scatter(df[x], y_data)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        self.view.figure.tight_layout()
        self.view.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.view.show()
    sys.exit(app.exec_())

