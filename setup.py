"""Command line utility for controlling Yamaha receivers."""
from setuptools import setup, find_packages

setup(
    name='rxvc',
    description=__doc__,
    version='0.1.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    author='Anthony Grimes',
    author_email='i@raynes.me',
    url='https://github.com/raynes/rxvc',
    license='MIT',
    install_requires=[
        'rxv==0.1.7',
        'click==6.2'
    ],
    entry_points='''
    [console_scripts]
    rxvc=rxvc.cli:cli
    '''
)
