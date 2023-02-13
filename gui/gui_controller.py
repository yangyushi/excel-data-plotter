import numpy as np  # for possible lambda transformation on Y
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


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
        file_name, _ = QFileDialog.getOpenFileName(
            self.view, "Load Data", "", "Excel Files (*.xlsx);;All Files (*)", options=options
        )
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

