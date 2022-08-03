from inspect import currentframe
from pathlib import Path
from shlex import quote
from subprocess import PIPE, STDOUT, run

from xptools.run import Attrs


def find_attrs():
    frame = currentframe().f_back
    while frame:
        for v in frame.f_locals.values():
            if isinstance(v, Attrs):
                return v
        frame = frame.f_back


def shell(*command, debug=False, **environ):
    args = " ".join((*(f"{k}={v}" for k, v in environ.items()), *map(str, command)))
    stdout = None if debug else PIPE
    print(f"[shell] {args}")
    process = run(args, shell=True, text=True, stdout=stdout, stderr=STDOUT)
    if process.returncode:
        output = process.stdout
        output and print(output.strip())
        exit(1)


def xpfix(src, dst=None, **kwargs):
    src = Path(src)
    dst = dst or src.parent / f".{src.name}"
    shell("xpfix", *(quote(f"{k}={v}") for k, v in kwargs.items()), "<", src, ">", dst)
    return dst
