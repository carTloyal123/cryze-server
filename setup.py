from setuptools import setup, find_packages

setup(
    name = 'cryze_server',
    version='0.0.11',

    #can list down each package names - no need to keep __init__.py under packages / directories
    packages=['cryze_server'], #importing is like: from package1 import mod2, or import package1.mod2 as m2

    license='GPLv3',

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],

    install_requires=[
        'websockets',
        'asyncio'
    ],

    # include test dependencies
    tests_require=['pytest']
)
