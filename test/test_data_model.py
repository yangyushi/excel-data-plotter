import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import numpy as np
import pandas as pd

import pytest

from data.data_model import DataModel

@pytest.fixture
def data_model():
    return DataModel()

def test_load_data(data_model):
    data = {
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9],
    }
    df = pd.DataFrame(data)
    df.to_excel("test_data.xlsx", index=False)
    data_model.load_data("test_data.xlsx")
    assert (data_model.df == df).all().all()
