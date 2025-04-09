# tests/test_io.py

import pandas as pd
from llamacancer.io import _load_datafile


def test_load_csv(tmp_path):
    # Create a sample CSV file
    data = "PatientID,TreatmentArm\nP1,CART\nP2,SOC\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(data)
    df = _load_datafile(str(file_path))
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2


def test_missing_file(tmp_path):
    file_path = tmp_path / "nonexistent.csv"
    df = _load_datafile(str(file_path))
    assert df is None
