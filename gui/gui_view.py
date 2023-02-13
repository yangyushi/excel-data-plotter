from PyQt5.QtWidgets import QMainWindow, QComboBox, QVBoxLayout,\
    QHBoxLayout, QLabel, QPushButton, QRadioButton, QLineEdit, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as\
    NavigationToolbar
from matplotlib.figure import Figure


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
        self.y_transform_edit.setFixedWidth(200)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('X-axis:'))
        hbox.addWidget(self.x_combo)
        hbox.addStretch(1)
        hbox.addWidget(QLabel('Y-axis:'))
        hbox.addWidget(self.y_combo)
        hbox.addStretch(1)
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

