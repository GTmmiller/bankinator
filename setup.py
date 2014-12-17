from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bankinator',
    version='1.0.0',
    description='A package that pulls transaction data from banking websites',
    long_description=long_description,
    url='https://github.com/GTmmiller/bankinator',
    author='Steven Miller',
    author_email='msm@gatech.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',

        'License :: OSI Approved :: MIT License',

        'Natural Language :: English',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only'
    ],
    keywords='banking api script internet',
    packages=find_packages(),
    install_reqires=['requests'],

    entry_points={
        'console_scripts': ['bankinate=bankinate:main']
    }
)