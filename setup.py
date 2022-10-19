from setuptools import find_packages, setup

name = "xprun"

setup(
    name=name,
    packages=find_packages(),
    entry_points=dict(
        console_scripts=[
            f"xprun={name}.run:Main.entrypoint",
        ]
    ),
)
