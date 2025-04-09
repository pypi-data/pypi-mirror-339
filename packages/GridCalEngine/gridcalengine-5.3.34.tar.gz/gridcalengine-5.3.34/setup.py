# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
"""
A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
import sys
import subprocess
import importlib
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
from GridCalEngine.__version__ import __GridCalEngine_VERSION__
from GridCalEngine.Compilers.circuit_to_gslv import GSLV_RECOMMENDED_VERSION

here = os.path.abspath(os.path.dirname(__file__))

long_description = """# GridCal

This software aims to be a complete platform for power systems research and simulation.

[Watch the video https](https://youtu.be/SY66WgLGo54)

[Check out the documentation](https://gridcal.readthedocs.io)


## Installation

pip install GridCalEngine

For more options (including a standalone setup one), follow the
[installation instructions]( https://gridcal.readthedocs.io/en/latest/getting_started/install.html)
from the project's [documentation](https://gridcal.readthedocs.io)
"""

description = 'GridCal is a Power Systems simulation program intended for professional use and research'

pkgs_to_exclude = ['docs', 'research', 'tests', 'tutorials', 'GridCal']

packages = find_packages(exclude=pkgs_to_exclude)

# ... so we have to do the filtering ourselves
packages2 = list()
for package in packages:
    elms = package.split('.')
    excluded = False
    for exclude in pkgs_to_exclude:
        if exclude in elms:
            excluded = True

    if not excluded:
        packages2.append(package)

package_data = {'GridCalEngine': ['LICENSE.txt', 'setup.py'], }

dependencies = ['setuptools>=41.0.1',
                'wheel>=0.37.2',
                "numpy<=2.0.0",
                "autograd>=1.7.0",
                "scipy>=1.0.0",
                "networkx>=2.1",
                "pandas>=2.2.3",
                "highspy>=1.8.0",
                "xlwt>=1.3.0",
                "xlrd>=1.1.0",
                "matplotlib>=2.1.1",
                "openpyxl>=2.4.9",
                "chardet>=3.0.4",  # for the psse files character detection
                "scikit-learn>=1.5.0",
                "geopy>=1.16",
                "pytest>=7.2",
                "h5py>=3.12.0",
                "numba>=0.60",  # to compile routines natively
                'pyproj',
                'pyarrow>=15',
                "windpowerlib>=0.2.2",
                "pvlib>=0.11",
                "rdflib",
                "pymoo>=0.6",
                "websockets",
                "brotli",
                "opencv-python>=4.10.0.84",
                ]

# Define a list of optional packages as dictionaries. Each dictionary
# specifies the module name to import and the pip spec to install.
optional_packages = [
    {
        "module": "pygslv",
        "spec": f"pygslv>={GSLV_RECOMMENDED_VERSION}"
    },
    {
        "module": "tables",
        "spec": f"tables"
    },
    # Add more optional packages here as needed.
    # For example:
    # {
    #     "module": "another_optional_module",
    #     "spec": "another_optional_module>=1.2.3"
    # },
]


# For each optional package, try to import, and if not present, attempt installation.
for dep in optional_packages:
    module_name = dep["module"]
    install_spec = dep["spec"]
    try:
        importlib.import_module(module_name)
        print(f"Optional dependency '{module_name}' is already installed.")
    except ImportError:
        print(f"Optional dependency '{module_name}' not found. Attempting to install '{install_spec}'...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', install_spec]
            )
            print(f"Successfully installed '{module_name}'.")
        except subprocess.CalledProcessError:
            print(
                f"Warning: Installation of optional dependency '{module_name}' failed. Continuing without it.")



setup(
    name='GridCalEngine',  # Required
    version=__GridCalEngine_VERSION__,  # Required
    license='MPL2',
    description=description,  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/SanPen/GridCal',  # Optional
    author='Santiago Peñate Vera et. Al.',  # Optional
    author_email='santiago@gridcal.org',  # Optional
    classifiers=[
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='power systems planning',  # Optional
    packages=packages2,  # Required
    package_dir={'': '.'},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=dependencies,
    package_data=package_data,
    # this attempts at installing the optional stuff without using the ridiculous pip optional notation

)


