from setuptools import find_packages, setup

pkgs = find_packages("src")

name = pkgs[0]

setup(
    entry_points={
        "console_scripts": [
            f"xprun={name}.run:Main.entrypoint",
        ],
    },
    name=name,
    packages=pkgs,
    package_dir={"": "src"},
)
