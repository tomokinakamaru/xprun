from pathlib import Path
from statistics import median
from subprocess import check_call
from sys import executable


def execute(attrs):
    name = "forloop-perf-scenario.py"
    path = Path(__file__).parent / name
    dest = attrs.outdir / name
    code = path.read_text()
    code = code.replace("__size__", str(attrs.size))
    code = code.replace("__outdir__", str(attrs.outdir))
    dest.write_text(code)
    check_call([executable, dest])


def extract(attrs):
    path = attrs.outdir / "time.txt"
    time = float(path.read_text())
    if attrs.scale == "s":
        yield "s", time / 1000
    elif attrs.scale == "ms":
        yield "ms", time
    else:
        raise Exception()


def visualize(data, attrs):
    for label in ("s", "ms"):
        _visualize(label, data, attrs)


def _visualize(label, data, attrs):
    filtered = data.filter(label=label)
    filtered = filtered.group("size")
    filtered = filtered.apply(lambda rs: median(r.value for r in rs))
    path = attrs.outdir / f"{attrs.name}-{label}.txt"
    with open(path, "w") as f:
        for size, val in filtered.items():
            print(f"10^{size}: {val:.2e}{label}", file=f)
