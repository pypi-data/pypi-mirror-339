from io import open
from setuptools import setup

"""
:authors: DPomortsev
:copyright: (c) 2021 DPomortsev
"""

version = "1.0.0"

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Urban-Transit-Network-Analysis',
    version=version,

    author='DPomortsev',
    author_email='danul78969@gmail.com',

    url='https://github.com/DanilPomortsev/Urban-Transit-Network-Analysis',

    description=(
        u'Python module for urban network analysis'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["Urban-Transit-Network-Analysis"],
    install_requires=['osmnx',
                      'requests',
                      'beautifulsoup4',
                      'neo4j',
                      'pandas',
                      'plotly',
                      'deep-translator',
                      'quads',
                      'numpy'
    ]
)

