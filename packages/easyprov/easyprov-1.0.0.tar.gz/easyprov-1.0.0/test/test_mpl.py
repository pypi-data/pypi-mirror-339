import matplotlib.pyplot as plt

from easyprov.prov_mpl import fig_dump


def test_prov_is_working(tmp_path):
    # fmt
    fig, axes = plt.subplots(1, 1, figsize=(6, 4), squeeze=False)
    ax = axes[0, 0]
    ax.plot([0, 1], [0, 1])
    fig.tight_layout()

    # save
    pth = tmp_path / "tmp_data.png"
    fig_dump(fig, pth, __file__)
    assert b"test_mpl.py" in open(pth, "rb").read()

    pth = tmp_path / "tmp_data.svg"
    fig_dump(fig, pth, __file__)
    assert "test_mpl.py" in open(pth, encoding="utf-8").read()
