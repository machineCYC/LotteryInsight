import os
from io import open

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="LotteryInsight",  # Required
    version='',  # Required
    description="taiwan lottery light",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/machineCYC",  # Optional
    author="linsam",  # Optional
    author_email="yenchen0416@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        # "Intended Audience :: Developers",
        # "Topic :: Software Development :: Buil Tools",
        # "License :: OSI Approved :: MIT License",
        # "Programming Language :: Python :: 3.6",
    ],
    keywords="lottery, python",  # Optional
    packages=find_packages(exclude=["importlib", "lxml", "loguru"]),
    project_urls={  # Optional
        "Source": "https://github.com/machineCYC/LotteryInsight",
    },
)
