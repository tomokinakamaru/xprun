from pathlib import Path
from re import compile
from sys import stdin
from textwrap import indent

from xptools.argparser import ArgParser


class Main(object):
    @classmethod
    def entrypoint(cls):
        cls().main()

    def __init__(self):
        self.args, unknown = parser.parse_known_args()
        self.xargs = xargs_parse(unknown)

    def main(self):
        lines = []
        lines += self.args.begin.splitlines() if self.args.begin else []
        lines += stdin.read().splitlines()
        lines += self.args.end.splitlines() if self.args.end else []
        for src, dst in self.xargs.items():
            lines = self.replace(lines, src, "\n".join(dst))
        for line in lines:
            print(line)

    def replace(self, lines, src, dst):
        for line in lines:
            d = dst
            if "\n" in d:
                i = len(head_spaces.match(line).group(0))
                d = indent(d, " " * i).strip()
            yield line.replace(src, d)


def xargs_parse(args):
    xargs = {}
    for arg in args:
        if "=" in arg:
            src, dst = arg.split("=", 1)
            xargs.setdefault(src, [])
            xargs[src].append(xargs_expand(dst))
        else:
            raise Exception(f'Invalid xarg "{arg}"')
    return xargs


def xargs_expand(val):
    if match := xargs_file_format.match(val):
        return Path(match.group(1)).read_text()
    else:
        return val


parser = ArgParser()

parser.add_argument("--begin", help="insert <text> at beginning", metavar="<text>")

parser.add_argument("--end", help="insert <text> at end", metavar="<text>")

xargs_file_format = compile(r"^@(.+)$")

head_spaces = compile(r"^\s*")
