from argparse import ArgumentParser
from argparse import HelpFormatter
from shutil import get_terminal_size


class ArgParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('formatter_class', Formatter)
        super().__init__(*args, **kwargs)


class Formatter(HelpFormatter):
    def __init__(self, prog):
        w = min(get_terminal_size().columns, 80)
        super().__init__(prog, width=w, max_help_position=w)
