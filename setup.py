from setuptools import find_packages  # type: ignore
from setuptools import setup  # type: ignore

name = 'xptools'

setup(
    name=name,
    packages=find_packages(),
    entry_points=dict(console_scripts=[
        f'xpfix={name}.fix:Main.entrypoint',
        f'xprun={name}.run:Main.entrypoint'
    ])
)
