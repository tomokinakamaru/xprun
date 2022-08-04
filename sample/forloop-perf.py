from statistics import median

from xptools import shell, xpfix


def run(attrs):
    scenario = xpfix(
        "sample/forloop-perf-scenario.py", __size__=attrs.size, __outdir__=attrs.outdir
    )
    shell("python", scenario)


def extract(attrs):
    path = attrs.outdir / "time.txt"
    yield "time", float(path.read_text())


def visualize(data, attrs):
    data = data.group("size")
    data = data.apply(lambda rs: median(r.value for r in rs))
    path = attrs.outdir / "result.txt"
    with open(path, "w") as f:
        for size, val in data.items():
            print(f"10^{size}: {val:.2e} sec.", file=f)
