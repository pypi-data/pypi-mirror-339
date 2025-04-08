import json

from easyprov.prov_json import json_dump, json_prov


def test_prov_is_working(tmp_path):
    # fmt
    data = {
        "toto": [1, 2, 3],
        "tutu": "atchoum"
    }

    # save
    pth = tmp_path / "tmp_data.json"
    json_dump(data, pth, __file__, indent=2)

    # read
    data = json.load(open(pth, "rb"))
    prov = json_prov(data)
    assert "test_json.py" in prov
