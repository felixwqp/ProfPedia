"""
Search server python package configuration.

Nilay Muchhala  <nilaym@umich.edu>
Aneeqa Fatima   <aneeqaf@umich.edu>
"""

from setuptools import setup

setup(
    name='profpedia',
    version='0.1.0',
    packages=['profpedia'],
    include_package_data=True,
    install_requires=[
        'bs4==0.0.1',
        'Flask==1.0.2',
        'Flask-Testing==0.7.1',
        'nodeenv==1.3.3',
        'pycodestyle==2.5.0',
        'pydocstyle==3.0.0',
        'pylint==2.3.1',
        'pytest==4.3.0',
        'requests==2.21.0',
        'selenium==3.141.0',
        'sh==1.12.14',
    ],
)
