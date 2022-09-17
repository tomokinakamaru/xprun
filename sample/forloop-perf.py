from pathlib import Path
from statistics import median
from sys import executable

from xptools import shell, xpfix
from xptools.utils import find_attrs, find_results


def execute(attrs):
    path = Path(__file__).parent / "forloop-perf-scenario.py"
    scenario = xpfix(path, __size__=attrs.size, __outdir__=attrs.outdir)
    shell(executable, scenario)


def extract(attrs):
    path = attrs.outdir / "time.txt"
    time = float(path.read_text())
    if attrs.scale == "s":
        yield "s", time / 1000
    elif attrs.scale == "ms":
        yield "ms", time
    else:
        raise Exception()


def visualize(results, attrs):
    for label in ("s", "ms"):
        _visualize(label)


def _visualize(label):
    results, attrs = find_results(), find_attrs()
    filtered = results.filter(label=label)
    filtered = filtered.group("size")
    filtered = filtered.apply(lambda rs: median(r.value for r in rs))
    path = attrs.outdir / f"{attrs.name}-{label}.txt"
    with open(path, "w") as f:
        for size, val in filtered.items():
            print(f"10^{size}: {val:.2e}{label}", file=f)
