from inspect import currentframe
from pathlib import Path
from shlex import quote
from subprocess import run
from sys import executable

from xptools.run import Attrs, Results


def find_attrs():
    return _find_object(Attrs)


def find_results():
    return _find_object(Results)


def shell(*command, **environ):
    args = " ".join((*(f"{k}={v}" for k, v in environ.items()), *map(str, command)))
    print(args)
    process = run(args, shell=True, text=True)
    if process.returncode:
        exit(1)


def xpfix(src, dst=None, begin=None, end=None, **kwargs):
    src = Path(src)
    if dst is None:
        if attrs := find_attrs():
            dst = attrs.outdir / src.name
        else:
            dst = src.parent / f".{src.name}"

    args = []

    for k, v in {"begin": begin, "end": end}.items():
        if v is not None:
            lst = v if isinstance(v, (list, tuple)) else [v]
            for e in lst:
                args.extend([f"--{k}", quote(str(e))])

    for k, v in kwargs.items():
        lst = v if isinstance(v, (list, tuple)) else [v]
        for e in lst:
            args.append(quote(f"{k}={e}"))

    shell(Path(executable).parent / "xpfix", *args, "<", src, ">", dst)
    return dst


def _find_object(cls):
    frame = currentframe().f_back
    while frame:
        for v in frame.f_locals.values():
            if isinstance(v, cls):
                return v
        frame = frame.f_back
