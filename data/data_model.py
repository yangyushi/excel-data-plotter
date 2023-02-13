import sys
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject

class DataModel(QObject):
    data_loaded = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.df = None

    def load_data(self, file_name):
        self.df = pd.read_excel(file_name)
        self.data_loaded.emit(self.df)

    def get_data(self):
        return self.df
