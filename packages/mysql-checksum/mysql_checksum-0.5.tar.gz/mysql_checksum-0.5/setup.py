from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mysql_checksum',
    author='demmonico',
    version='0.5',
    long_description=long_description,
    long_description_type="text/markdown",

    packages=find_packages(),

    install_requires=[
    ],

    entry_points={
        'console_scripts': [
            'mysql-checksum = mysql_checksum:hello',
        ],
    },
)
        #'mysql-connector-python',
        #'logging'
