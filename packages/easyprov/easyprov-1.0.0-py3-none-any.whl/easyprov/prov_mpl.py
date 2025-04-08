"""
Store provenance in figures generated using matplotlib
"""
from pathlib import Path

from .provenance import fmt_prov


def fig_dump(data, pth, pth_script, **kwds):
    """Write figure in svg|png file.

    Args:
        data (matplotlib.Figure): data to write
        pth (str|Path): path to file to write
        pth_script (str|Path): path to script that generated data
        **kwds: additional arguments that will be passed to savefig

    Returns:
        None
    """
    file_ext = Path(pth).name.split(".")[-1]
    assert file_ext in ["svg", "png"]

    data.savefig(pth, metadata={"Creator": fmt_prov(pth_script)}, **kwds)


def fig_prov(pth):
    """Read provenance in file.

    Args:
        pth (Path): path to file to read (previously saved with rst_dump)

    Returns:
        (str): provenance, path to script that generated data
    """
    raise NotImplementedError(f"not implemented for path '{pth}'")
