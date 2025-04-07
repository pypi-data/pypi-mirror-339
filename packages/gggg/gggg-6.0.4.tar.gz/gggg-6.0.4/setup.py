from setuptools import setup, find_packages

setup(
    name="gggg",
    version="6.0.4",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "gen-gmail = gggg.cli:main",
        ],
    },
)