import io
import os
import sys
from pathlib import Path

from setuptools import setup, find_packages

install_requires = ["six==1.*", "numpy>=2.0.0", "networkx==2.*", 'pandas>=1.0.0', 'rdkit', 'tqdm']

if sys.version_info < (3, 4, 0):
    install_requires.append("enum34")


def get_version():
    with open(os.path.join("mordred", "_version.txt")) as f:
        return f.read().strip()


def get_test_data():
    for p, _, fs in os.walk(os.path.join("mordred", "tests", "references")):
        p = p.split(os.sep)[2:]

        for f in fs:
            yield os.path.join(*(p + [f]))


README_rst = ""
fndoc = os.path.join(os.path.dirname(__file__), "README.rst")
with io.open(fndoc, mode="r", encoding="utf-8") as fd:
    README_rst = fd.read()

setup(
    name="mordred-ojmb",
    version=get_version(),
    description="molecular descriptor calculator",
    long_description= README_rst,
    long_description_content_type='text/x-rst',
    license="BSD-3-Clause",
    author="Hirotomo Moriwaki",
    author_email="philopon.dependence@gmail.com",
    maintainer="Olivier J. M. Béquignon",
    maintainer_email="olivier.bequignon.maintainer@gmail.com",
    url="https://github.com/OlivierBeq/mordred",
    platforms=["any"],
    keywords="QSAR chemoinformatics",
    packages=find_packages(),
    package_data={
        "mordred": ["data/*.txt", "_version.txt"],
        "mordred.tests": list(get_test_data()),
    },
    install_requires=install_requires,
    tests_require=["nose==1.*", "PyYaml>=4.2b1"],
    extras_require={"mordred": ["pandas", "tqdm", "rdkit"]},
    cmdclass={"test": None},
)
