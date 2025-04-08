import pandas as pd

from easyprov.prov_csv import csv_dump, csv_header, csv_prov


def test_prov_is_working(tmp_path):
    data = pd.DataFrame([dict(a=1, b=2, c=3)] * 3).set_index("a")
    header = {
        "a": "[#] toto",
        "b": "[°C] titi",
        "c": "[rad] tutu",
    }
    # save
    pth = tmp_path / "tmp_data.csv"
    csv_dump(data, header, pth, __file__)

    # read
    prov = csv_prov(pth)
    assert "test_csv.py" in prov
    header = csv_header(pth)
    assert "a" in header
    assert "b" in header
    assert "c" in header
