import setuptools
from datakorea.version_info import __version__, __author__, __email__, __project__

with open("requirements.txt") as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__project__,
    version=__version__,
    license='MIT',
    author=__author__,
    author_email=__email__,
    description="Korea Rest API data library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kukjinman/datakorea",
    packages=setuptools.find_packages(),
    keywords=['data', 'datakorea', 'restapi', 'python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=install_requires,
)