"""
pyPreservica.Gov setup

author:     James Carr
licence:    Apache License 2.0

"""

import pathlib
import sys
import os
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PKG = "pyPreservicaGov"

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


# This call to setup() does all the work
setup(
    name=PKG,
    version="1.0.1",
    description="Python Library For Harvesting Modern.Gov Records into Preservica for Long Term Preservation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://pypreservicagov.readthedocs.io/",
    author="James Carr",
    author_email="drjamescarr@gmail.com",
    include_package_data=True,
    package_data={'pyPreservicaGov': ['images/*.png', 'schema/*.xml', 'schema/*.xsd', 'schema/*.xsl']},
    license="Apache License 2.0",
    packages=["pyPreservicaGov"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving",
    ],
    keywords='Preservica API Preservation Modern.Gov Civica',
    install_requires=["pyPreservica", "python-dateutil", "bs4", "pathvalidate", "readchar"],
    project_urls={
        'Documentation': 'https://pypreservicagov.readthedocs.io/',
        'Source': 'https://github.com/carj/pyPreservica.Gov',
        'Discussion Forum': 'https://groups.google.com/g/pyPreservicaGov',
    }
)
