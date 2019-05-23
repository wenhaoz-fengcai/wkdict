import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wkdict",
    version="0.1.0",
    author="Wenhao Zhang",
    author_email="wenhaoz@ucla.edu",
    description="A dictionary app sits in your CLI environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiaowoshabi/wkdict",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "requests",
        "wiktionaryparser"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['wkdict=wkdict.command:main'],
    }
)
