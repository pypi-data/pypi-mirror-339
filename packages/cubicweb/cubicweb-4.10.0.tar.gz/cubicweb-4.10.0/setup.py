#!/usr/bin/env python
# pylint: disable=W0142,W0403,W0404,W0613,W0622,W0622,W0704,R0904,C0103,E0611
#
# copyright 2003-2025 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""Generic Setup script, takes package info from __pkginfo__.py file"""

from os.path import dirname, join

from setuptools import setup, find_packages

here = dirname(__file__)

# import required features
pkginfo = join(here, "cubicweb", "__pkginfo__.py")
__pkginfo__ = {}
with open(pkginfo) as f:
    exec(f.read(), __pkginfo__)
modname = __pkginfo__["modname"]
version = __pkginfo__["version"]
license = __pkginfo__["license"]
description = __pkginfo__["description"]
web = __pkginfo__["web"]
author = __pkginfo__["author"]
author_email = __pkginfo__["author_email"]

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

# import optional features
distname = __pkginfo__["distname"]
package_data = __pkginfo__["package_data"]

setup(
    name=distname,
    version=version,
    license=license,
    url=web,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
    install_requires=[
        "logilab-common >= 1.9.7, < 2.0.0",
        "logilab-mtconverter >= 0.9.2, < 1.0.0",
        "rql >= 0.41.0, < 1.0.0",
        "yams >= 0.50.0, < 1.0.0",
        "lxml >= 5.2.0, < 6.0.0",
        "lxml_html_clean >= 0.4.1",
        "logilab-database >= 1.20.0, < 2.0.0",
        "passlib >= 1.7",
        "pytz",
        "Markdown >= 3.4.0",
        "filelock",
        "rdflib >= 6.0.0",
        "pyramid >= 1.10.8, < 2.0.0",
        "waitress >= 2.1.2, <  3.0.0; python_version <  '3.8'",
        "waitress >= 2.1.2, <= 3.0.0; python_version == '3.8.*'",
        "waitress >= 3.0.2, <  4.0.0; python_version >= '3.9'",
        "wsgicors >= 0.3",
        "pyramid_multiauth < 1.0.0",  # to remove with Pyramid 2
        "repoze.lru",
        "cachetools",
        "importlib_metadata; python_version < '3.10'",
    ],
    entry_points={
        "console_scripts": [
            "cubicweb-ctl = cubicweb.cwctl:run",
        ],
        "paste.app_factory": [
            "pyramid_main=cubicweb.pyramid:pyramid_app",
        ],
    },
    extras_require={
        "captcha": [
            "Pillow",
        ],
        "crypto": [
            "pycryptodomex",
        ],
        "ext": [
            "docutils >= 0.6",
        ],
        "ical": [
            "vobject >= 0.6.0",
        ],
        "postgresql": [
            "psycopg2-binary",
        ],
        "s3": [
            "minio",
        ],
    },
    zip_safe=False,
    python_requires=">=3.7",
)
