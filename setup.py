from setuptools import setup, find_packages

setup(
    name='nontransitive-dice',
    version='0.0.1',
    packages=find_packages(exclude=['testing']),

    # Dependencies
    install_requires=[
        'numpy',
    ],

    # Metadata for PyPI
    author='David Hall',
    license='MIT',
    url='https://github.com/davidchall/nontransitive-dice',
)
