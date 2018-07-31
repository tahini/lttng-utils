#!/usr/bin/env python3
#
# The MIT License (MIT)
#
# Copyright (C) 2018 - Geneviève Bastien <gbastien@versatic.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""LTTng-utils setup script"""

import shutil
import sys
from setuptools import setup

if sys.version_info[0:2] < (3, 4):
    raise RuntimeError("Python version >= 3.4 required.")

if 'install' in sys.argv:
    if shutil.which('lttng') is None:
        print('lttng-utils is a helper for lttng and lttng should be available on the system.\n'
              'See https://www.lttng.org for more info.',
              file=sys.stderr)
        sys.exit(1)

setup(
    name='lttng-utils',
    version="0.1",

    description='LTTng-utils provides helper scripts for lttng tracing',

    url='https://github.com/tahini/lttng-utils',

    author='Geneviève Bastien',
    author_email='gbastien@versatic.net',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
    ],

    keywords='lttng tracing',

    packages=[
        'lttngutils',
        ],

    scripts=[
        'lttng-record-trace'
    ],

    install_requires=[
        'pyyaml',
    ],

    include_package_data = True

)
