import pandas as pd

class DataModel:
    def __init__(self):
        self.df = None

    def load_data(self, file_name):
        self.df = pd.read_excel(file_name)
    
    def get_data(self):
        return self.df
