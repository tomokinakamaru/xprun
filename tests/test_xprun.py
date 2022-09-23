from pathlib import Path
from subprocess import check_call
from sys import executable


def test_xprun():
    xprun = str(Path(executable).parent / "xprun")
    params = "sample/forloop-perf.json"
    script = "sample/forloop-perf.py"
    check_call([xprun, "-f", "-p", params, script])
