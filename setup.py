from setuptools import setup
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as f:
    readme = f.read()

about = {}
with open(os.path.join(here, "chromie", "__version__.py"), "r") as f:
    exec(f.read(), about)

if sys.argv[-1] == "test":
    os.system("python -m unittest")
    sys.exit()
elif sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/* --skip-existing")
    sys.exit()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    packages=["chromie"],
    long_description_content_type="text/markdown",
    url="https://github.com/Sandersland/chromie",
    author=about["__author__"],
    author_email=about["__email__"],
    license=about["__license__"],
    extras_require={"dev": ["twine", "black"]},
    install_requires=["requests==2.24.0", "cryptography==3.0", "PyJWT==1.7.1"],
    entry_points={"console_scripts": ["chromie=chromie:main"]},
)
