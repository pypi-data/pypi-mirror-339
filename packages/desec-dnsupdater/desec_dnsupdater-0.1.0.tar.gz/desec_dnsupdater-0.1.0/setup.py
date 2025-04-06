# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['desec_dyndns']
install_requires = \
['click>=8.1.8,<9.0.0', 'desec-dns==1.2.0', 'ifaddr>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['desec-dyndns = desec_dyndns:update']}

setup_kwargs = {
    'name': 'desec-dnsupdater',
    'version': '0.1.0',
    'description': 'A simple DynDNS client for deSEC.io',
    'long_description': '',
    'author': 'Ole Langbehn',
    'author_email': 'ole@langbehn.family',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11',
}


setup(**setup_kwargs)
