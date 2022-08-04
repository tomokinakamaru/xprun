from xptools.utils import shell


def test_xprun():
    shell("xprun", "-f", "-p", "sample/forloop-perf.json", "sample/forloop-perf.py")
