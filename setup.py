# The MIT License
#
# Copyright (c) 2014- High-Mobility GmbH (https://high-mobility.com)
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from distutils.core import setup, Extension
from io import open
#from setuptools import setup, Extension

with open("README.md", "r") as fh:
    _long_description = fh.read()

setup(
    name = 'hmkit',
    version = '0.1',
    description='High Mobility Python Bluetooth SDK',
    license='MIT License',
    author='High-Mobility GmbH',
    long_description=_long_description,
    url='https://github.com/highmobility/hm-python-bt-sdk',
    packages=['hmkit', 'hmkit.autoapi', 'hmkit.autoapi.commands', 'hmkit.autoapi.properties', 'hmkit.autoapi.properties.component', 'hmkit.autoapi.properties.value', 'hmkit.autoapi.properties.value.charging'],
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)

setup(
    name = 'hm_pyc',
    version = '0.1',
    description='High Mobility Python Bluetooth SDK lib extension',
    license='MIT License',
    author='High-Mobility GmbH',
    url='https://github.com/highmobility/hm-python-bt-sdk',
    ext_modules = [Extension('hmkit.hm_pyc', ['hmkit/hm_pyc/pyc_extension_module.c'], library_dirs=['/usr/lib'], libraries=['hmlink'] )],
    package_data={'': ['libhmlink.so']},
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
