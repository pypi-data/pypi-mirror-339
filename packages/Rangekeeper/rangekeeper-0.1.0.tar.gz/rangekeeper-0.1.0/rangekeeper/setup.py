from setuptools import setup

setup(
    name='Rangekeeper',
    version='0.2.0-alpha',
    packages=['models', 'dynamics'],
    package_dir={'': 'rangekeeper'},
    url='https://github.com/daniel-fink/rangekeeper',
    license='MPL-2.0',
    author='Daniel Fink',
    author_email='danfink@mit.edu',
    description='Rangekeeper is a library assisting financial modelling in real estate scenario planning, decision-making, cashflow forecasting, and the like.'
    )

