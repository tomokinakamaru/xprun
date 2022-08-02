from pathlib import Path
from subprocess import PIPE, STDOUT, run


def shell(*args, **kwargs):
    command = " ".join((*(f"{k}={v}" for k, v in kwargs.items()), *map(str, args)))
    print(f"[shell] {command}")
    process = run(command, shell=True, text=True, stdout=PIPE, stderr=STDOUT)
    if process.returncode:
        output = process.stdout.strip()
        output and print(output)
        exit(1)


def xpfix(src, dst=None, **kwargs):
    src = Path(src)
    dst = dst or src.parent / f".{src.name}"
    shell("xpfix", *(f"'{k}={v}'" for k, v in kwargs.items()), "<", src, ">", dst)
    return dst
