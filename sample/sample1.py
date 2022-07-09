from xptools import xpfix
from xptools import shell
from statistics import median


def run(attrs):
    scenario = xpfix(
        'sample/sample1-scenario.py',
        __size__=attrs.size,
        __outdir__=attrs.outdir
    )
    shell('python', scenario)


def extract(attrs):
    path = attrs.outdir / 'time.txt'
    yield 'time', float(path.read_text())


def visualize(data, attrs):
    data = data.group('size')
    path = attrs.outdir / 'result.txt'
    with open(path, 'w') as f:
        for size, rs in data.items():
            t = median(r.value for r in rs)
            print(f'{size}: {t:.2e}', file=f)
