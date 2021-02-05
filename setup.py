#!/usr/bin/env python3
import os
import re
import sys

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
Requires Python {}.{}, but you're trying
to install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('babel_transpiling')

setup(
    name='django-babel_transpiling',
    version=version,
    url='https://github.com/DistPub/django-babel-transpiling',
    license='MIT',
    description='Bring babel to your django project, transpiling static .jsx files on the fly, without NodeJS require!',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Smite Chow',
    author_email='xiaopengyou2no1@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['whitenoise', 'py_mini_racer'],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
