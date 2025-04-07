# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mandelshtam',
 'mandelshtam.internal',
 'mandelshtam.internal.interfaces',
 'mandelshtam.internal.levenshtein']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mandelshtam',
    'version': '0.0.0',
    'description': 'String similarity algorithms. Levenshtein, and more.',
    'long_description': '# mandelshtam\n\n[![PyPI Version][shields/pypi/version]][pypi/homepage]\n[![PyPI Downloads][shields/pypi/downloads]][pypi/homepage]\n[![License][shields/pypi/license]][github/license]\n[![Python Version][shields/python/version]][pypi/homepage]\n\n<p align="center">\n  <picture align="center">\n    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/syubogdanov/mandelshtam/02b751c47a03744fcba8d69d32b6f8a8a771c881/images/performance-dark.svg">\n    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/syubogdanov/mandelshtam/02b751c47a03744fcba8d69d32b6f8a8a771c881/images/performance-light.svg">\n    <img alt="Shows a bar chart with benchmark results." src="https://raw.githubusercontent.com/syubogdanov/mandelshtam/02b751c47a03744fcba8d69d32b6f8a8a771c881/images/performance-dark.svg">\n  </picture>\n</p>\n\n<p align="center">\n  <i>Levenshtein: "The Call of Cthulhu" vs "The Metamorphosis".</i>\n</p>\n\n## Key Features\n\n* Performance of *C* extensions;\n* GIL-free & Dependency-free;\n* Supports Python 3.9+.\n\n## Getting Started\n\n### Installation\n\nThe library is available as [`mandelshtam`][pypi/homepage] on PyPI:\n\n```shell\npip install mandelshtam\n```\n\n### Usage\n\n#### Levenshtein\n\nFor more, see the [documentation][docs/levenshtein].\n\n```python\nfrom mandelshtam import levenshtein\n\ns1 = "mandelshtam"\ns2 = "levenshtein"\n\nassert levenshtein(s1, s2) == 8\n```\n\n## License\n\nMIT License, Copyright (c) 2025 Sergei Y. Bogdanov. See [LICENSE][github/license] file.\n\n<!-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -->\n\n[docs/levenshtein]: https://mandelshtam.readthedocs.io/en/latest/levenshtein.html\n\n[github/license]: https://github.com/syubogdanov/mandelshtam/tree/main/LICENSE\n\n[pypi/homepage]: https://pypi.org/project/mandelshtam/\n\n[shields/pypi/downloads]: https://img.shields.io/pypi/dm/mandelshtam.svg?color=green\n[shields/pypi/license]: https://img.shields.io/pypi/l/mandelshtam.svg?color=green\n[shields/pypi/version]: https://img.shields.io/pypi/v/mandelshtam.svg?color=green\n[shields/python/version]: https://img.shields.io/pypi/pyversions/mandelshtam.svg?color=green\n',
    'author': 'Sergei Y. Bogdanov',
    'author_email': 'syubogdanov@outlook.com',
    'maintainer': 'Sergei Y. Bogdanov',
    'maintainer_email': 'syubogdanov@outlook.com',
    'url': 'https://github.com/syubogdanov/mandelshtam',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.14',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
