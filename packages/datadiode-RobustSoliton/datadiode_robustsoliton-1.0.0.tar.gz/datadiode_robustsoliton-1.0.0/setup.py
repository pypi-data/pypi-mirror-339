from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datadiode-RobustSoliton",
    version="1.0.0",
    author="Alin-Adrian Anton",
    author_email="alin.anton@upt.ro",
    description="Reliable one-way file transfer using Robust Soliton fountain codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BANPUMP-team/datadiode-RobustSoliton",
    package_dir={"datadiode_RobustSoliton": "src"},
    packages=["datadiode_RobustSoliton"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: Communications :: File Sharing",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.20.0",
        "tqdm>=4.62.0",
    ],
    entry_points={
        "console_scripts": [
            "datadiode-RobustSoliton=datadiode_RobustSoliton.__main__:main",
        ],
    },
)
