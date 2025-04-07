from setuptools import setup, find_packages

setup(
    name="gggg",
    version="1.0.8",
    author="Golden",
    packages=find_packages(),
    install_requires=["requests", "rich"],
    entry_points={
        "console_scripts": [
            "gen-gmail = gggg.cli:main",
        ],
    },
)