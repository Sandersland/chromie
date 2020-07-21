from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chromie",
    version="0.1.5",
    long_description=long_description,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sandersland/chromie",
    author="Steffen Andersland",
    author_email="stefandersland@gmail.com",
    license="MIT",
    extras_require={"dev": ["twine"]},
    entry_points={"console_scripts": ["chromie=chromie:main"]},
)
