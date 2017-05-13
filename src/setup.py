# -*- encoding: utf-8 -*-
'''
Created on 2016年5月31日

@author: hua
'''


from setuptools import setup, find_packages
import os
import re
import sys


version = re.compile(r'VERSION\s*=\s*\((.*?)\)')

def get_package_version():
    "returns package version without importing it"
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "cabbage/__init__.py")) as initf:
        for line in initf:
            m = version.match(line.strip())
            if not m:
                continue
            return ".".join(m.groups()[0].split(", "))


def get_requirements(filename):
    return open('requirements/' + filename).read().splitlines()


classes = """
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Topic :: System :: Distributed Computing
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.6
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]


install_requires = get_requirements('default.txt')
if sys.version_info < (3, 0):
    install_requires.append('futures')


setup(
    name='cabbage',
    version=get_package_version(),
    description='Celery cabbage',
#     long_description=open('README.rst').read(),
    author='huawei',
    author_email='alonelaval@gmail.com,120huawei@163.com',
    url='https://github.com/alonelaval/cabbage',
    license='BSD',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'test.*']),
    install_requires=install_requires,
    namespace_packages=["cabbage"],
#     test_suite="tests",
#     tests_require=get_requirements('test.txt'),
#     package_data={'fcabbage': ['templates/*', 'static/*.*',
#                              'static/**/*.*', 'static/**/**/*.*']},
    entry_points={
#         'console_scripts': [
#             'cabbage = cabbage.__main__:main',
#         ],
    },
)