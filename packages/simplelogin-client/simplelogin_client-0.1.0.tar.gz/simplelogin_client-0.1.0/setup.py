from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simplelogin-client",
    version="0.1.0",
    py_modules=["simplelogin"],
    install_requires=["requests"],
    author="Genesis Chrome",
    author_email="gnschrm@gmail.com",
    description="A Python client for interacting with the SimpleLogin API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChromeGenesis/simplelogin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
