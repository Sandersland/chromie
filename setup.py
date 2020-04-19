from setuptools import setup

with open ("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chromie",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sandersland/chromie",
    author="Steffen Andersland",
    author_email="stefandersland@gmail.com",
    license="MIT",
    extras_require={
        "dev": ["twine"]
    },
    entry_points={"console_scripts": ["chromie=chromie:main"]}
)