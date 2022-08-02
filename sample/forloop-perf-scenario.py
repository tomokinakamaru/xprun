# flake8: noqa
# type: ignore
from pathlib import Path
from time import time

start = time()

for _ in range(10**__size__):
    pass

Path("__outdir__/time.txt").write_text(str(time() - start))
