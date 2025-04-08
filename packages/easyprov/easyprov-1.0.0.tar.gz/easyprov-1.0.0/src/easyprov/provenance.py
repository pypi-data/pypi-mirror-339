"""
Set of function to write provenance in conventional files
"""

from pathlib import Path


def _prov_from_git(pth):
    in_between = []
    for fld in pth.parents[:-1]:
        git_dir = fld / ".git"
        if not git_dir.exists():
            in_between.append(fld.name)
        else:
            lines = [line.strip() for line in open(git_dir / "config").readlines() if len(line.strip()) > 0]
            for i, line in enumerate(lines):
                if line.startswith("[remote"):
                    for subline in lines[i + 1:]:
                        if subline.startswith("url = "):
                            url = subline.split(" = ")[-1]
                            prov = url.split("/")[-1][:-4]
                            for name in reversed(in_between):
                                prov += f"/{name}"

                            return prov + f"/{pth.name}"

                    return None

            return None

    return None


def fmt_prov(pth):
    """Format pth as a useful provenance

    Args:
        pth (str|Path): pth to shorten

    Returns:
        (str)
    """
    pth = Path(pth)
    prov = _prov_from_git(pth)
    if prov is not None:
        return prov

    parts = list(pth.parts)
    try:
        ind = parts.index("script")
        if ind == 0:
            return "/".join(parts[ind + 1:])

        return "/".join(parts[ind - 1:])
    except ValueError:
        return parts[-1]
