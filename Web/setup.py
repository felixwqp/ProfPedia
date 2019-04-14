"""
Index server python package configuration.

Nilay Muchhala  <nilaym@umich.edu>
Aneeqa Fatima   <aneeqaf@umich.edu>
"""

from setuptools import setup

setup(
    name='index',
    version='0.1.0',
    packages=['index'],
    include_package_data=True,
    install_requires=[
        'Flask==1.0.2',
        'pycodestyle==2.5.0',
        'pydocstyle==3.0.0',
        'pylint==2.3.1',
        'pytest==4.3.0',
        'sh==1.12.14',
    ],
)
