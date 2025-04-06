# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ros2_mypypkg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ros2-mypypkg',
    'version': '0.1.0',
    'description': 'ros2_py_learn',
    'long_description': None,
    'author': 'NopTop',
    'author_email': '439964032@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
