from pathlib import Path
from sys import executable

from xptools.utils import shell


def test_xprun():
    xprun = Path(executable).parent / "xprun"
    shell(xprun, "-f", "-p", "sample/forloop-perf.json", "sample/forloop-perf.py")
