from setuptools import setup, find_packages

from chromie import __version__, __author__, __email__, __license__


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chromie",
    version=__version__,
    long_description=long_description,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sandersland/chromie",
    author=__author__,
    author_email=__email__,
    license=__license__,
    extras_require={"dev": ["twine", "black"]},
    install_requires=["requests==2.24.0", "cryptography==3.0", "PyJWT==1.7.1"],
    entry_points={"console_scripts": ["chromie=chromie:main"]},
)
