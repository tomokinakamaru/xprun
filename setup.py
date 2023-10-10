from setuptools import setup

setup(
    entry_points={"console_scripts": ["xprun=xprun.run:Main.entrypoint"]},
    name="xprun",
)
