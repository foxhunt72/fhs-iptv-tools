import io
import os
import re

from setuptools import find_packages
from setuptools import setup


about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'src', 'fhs_iptv_tools', '__version__.py')) as f:
    exec(f.read(), about)


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


with open("./requirements.txt") as requirements:
    REQUIREMENTS = requirements.read().splitlines()


setup(
    name="fhs-iptv-tools",
    version=about["__version__"],
    url="https://github.com/foxhunt72/fhs-iptv-tools",
    license="MIT license",
    author="Richard de Vos",
    author_email="rdevos72@gmail.com",
    description="foxhunt software iptv tools, making iptv easier",
    long_description=read("README.rst"),
    entry_points={
        "console_scripts": [
            "fhs-iptv-tools=fhs_iptv_tools.cli:main",
        ],
    },

    packages=find_packages(
        where="src",
        exclude=(
            "tests",
            "tests_*",
        )
    ),
    package_dir={"": "src"},
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

