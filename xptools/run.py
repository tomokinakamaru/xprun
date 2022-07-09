from argparse import Namespace
from functools import cached_property
from hashlib import md5
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from itertools import product
from pathlib import Path
from re import compile
from shutil import rmtree
from .argparser import ArgParser


class Main(object):
    @classmethod
    def entrypoint(cls):
        cls().main()

    def __init__(self):
        self.args, unknown = parser.parse_known_args()
        self.xargs = xargs_parse(unknown)
        self.results = Results()

    @cached_property
    def script(self):
        p = self.args.script
        s = spec_from_file_location(p.stem, p)
        m = module_from_spec(s)
        s.loader.exec_module(m)
        return m

    @cached_property
    def outdir(self):
        return self.args.outdir or self.args.script.with_suffix('')

    def main(self):
        for run_attrs in self.attrs('run'):
            self.run(run_attrs)
            for sum_attrs in self.attrs('sum'):
                self.summarize(run_attrs, sum_attrs)
        for agg_attrs in self.attrs('agg'):
            self.aggregate(agg_attrs)

    def run(self, attrs):
        outdir = self.outdir / self.md5(attrs)
        success_file = outdir / success_file_name
        if self.args.force or not success_file.exists():
            attrs_file = outdir / attrs_file_name
            outdir.exists() and rmtree(outdir)
            outdir.mkdir(parents=True)
            attrs_file.write_text(self.dump(attrs))
            self.script.run(Namespace(outdir=outdir, **attrs))
            success_file.write_text('')

    def summarize(self, run_attrs, sum_attrs):
        outdir = self.outdir / self.md5(run_attrs)
        ns = Namespace(outdir=outdir, **run_attrs, **sum_attrs)
        for label, value in self.script.summarize(ns):
            self.results.append(Result(
                label=label, value=value,
                **run_attrs, **sum_attrs
            ))

    def aggregate(self, attrs):
        ns = Namespace(outdir=self.outdir, **attrs)
        self.script.aggregate(self.results, ns)

    def attrs(self, step):
        if dct := self.xargs.get(step):
            keys = tuple(dct)
            for vals in product(*dct.values()):
                yield dict(zip(keys, vals))
        else:
            yield {}

    def md5(self, dct):
        return md5(str(sorted(dct.items())).encode()).hexdigest()

    def dump(self, dct):
        return '\n'.join(f'{k} = {v}' for k, v in sorted(dct.items()))


class Results(list):
    def filter(self, **kwargs):
        rs = Results()
        for r in self:
            if r.test(**kwargs):
                rs.append(r)
        return rs

    def group(self, *keys):
        gr = GroupedResults()
        for r in self:
            d = gr
            for k in keys[:-1]:
                v = getattr(r, k)
                d = d.setdefault(v, GroupedResults())
            v = getattr(r, keys[-1])
            d.setdefault(v, []).append(r)
        return gr


class GroupedResults(dict):
    def apply(self, func):
        gr = GroupedResults()
        for k, v in self.items():
            if isinstance(v, GroupedResults):
                gr[k] = v.apply(func)
            else:
                gr[k] = func(v)
        return gr


class Result(Namespace):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def test(self, **kwargs):
        for name, pred in kwargs.items():
            val = getattr(self, name)
            if callable(pred) and not pred(val):
                return False
            elif val != pred:
                return False
        return True


def xargs_parse(args):
    xargs, names = {}, {}
    for arg in args:
        if match := xargs_format.match(arg):
            step, name, val = match.groups()
            if name in ('label', 'outdir', 'value'):
                raise Exception(f'"{name}" is reserved')
            if name in names and names[name] != step:
                raise Exception(f'Duplicate name "{name}"')
            dct = xargs.setdefault(step, {})
            lst = dct.setdefault(name, [])
            lst.extend(xargs_expand(val))
            names[name] = step
        else:
            raise Exception(f'Invalid xarg "{arg}"')
    return xargs


def xargs_expand(val):
    if match := xargs_range_format.match(val):
        start, end = map(int, match.groups())
        yield from range(start, end + 1)
    else:
        for text in val.split(','):
            for func in (int, float, str):
                try:
                    yield func(text)
                    break
                except ValueError:
                    pass


xargs_format = compile(r'^(run|sum|agg):(.+?)=(.+?)$')

xargs_range_format = compile(r'^(\d+)\.\.(\d+)$')

attrs_file_name = '.attrs'

success_file_name = '.success'

parser = ArgParser()

parser.add_argument(
    'script', help='path to script',
    metavar='<script>', type=Path
)

parser.add_argument(
    '-f', '--force',
    help='overwrite existing results',
    action='store_true'
)

parser.add_argument(
    '-o', '--outdir',
    help='path to output',
    metavar='<outdir>', type=Path
)
