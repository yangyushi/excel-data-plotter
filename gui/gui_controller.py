import numpy as np  # for possible lambda transformation on Y
from PyQt5.QtCore import QObject
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog, QLabel, QComboBox


class Controller(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.view.load_button.clicked.connect(self.load_data)
        self.view.plot_button.clicked.connect(self.plot_data)
        self.model.data_loaded.connect(self.data_loaded)
        self.view.add_column_button.clicked.connect(self.add_column)

        self.selected_columns = []

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
        self.view.add_column_button.setEnabled(True)
        self.view.plot_button.setEnabled(True)
        self.selected_columns = [self.view.y_combo]

    def add_column(self):
        column_combo = QComboBox()
        column_combo.addItems(list(self.model.get_data().columns))
        self.view.columns_layout.addWidget(QLabel('Select Column:'))
        self.view.columns_layout.addWidget(column_combo)
        self.selected_columns.append(column_combo)
        
    def plot_data(self):
        x = self.view.x_combo.currentText()
        y_transform = self.view.y_transform_edit.text()
        df = self.model.get_data()

        self.view.figure.clear()
        fig = self.view.figure
        axs = fig.subplots(
            len(self.selected_columns), 1, sharex=True,
            #figsize=(6, 4 * len(self.selected_columns))
        )
        if len(self.selected_columns) == 1:
            axs = [axs]
        if y_transform:
            try:
                y_transform = eval(f"lambda y: {y_transform}")
            except:
                y_transform = None

        for ax, combo_box in zip(axs, self.selected_columns):
            y = combo_box.currentText()
            y_data = df[y]
            if y_transform:
                y_data = y_transform(y_data)
            if self.view.line_plot_button.isChecked():
                ax.plot(df[x], y_data)
            else:
                ax.scatter(df[x], y_data)
            ax.set_ylabel(y)

        axs[-1].set_xlabel(x)
        fig.tight_layout()
        self.view.canvas.draw()
        self.view.canvas.flush_events()
        self.view.canvas.draw()