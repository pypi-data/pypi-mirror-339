from easyprov.prov_rst import rst_dump, rst_prov


def test_prov_is_working(tmp_path):
    txt = """
    Toto
    ====

    .. warning:: just some example

    todo
    """
    # save
    pth = tmp_path / "tmp_data.rst"
    rst_dump(txt, pth, __file__)

    # read
    prov = rst_prov(pth)
    assert "test_rst.py" in prov
