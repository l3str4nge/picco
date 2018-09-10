import setuptools
from pip.req import parse_requirements
from picco import __version__, __name__

requirements = [str(i.req) for i in parse_requirements('requirements.txt', session=False)]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__name__,
    version=__version__,
    author="Mateusz Zawadzki",
    author_email="mtszzwdzk@gmail.com",
    description="Tool for backup your images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mateuszz0000/picco",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
