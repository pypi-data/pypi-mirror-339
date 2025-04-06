from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='mysql_checksum',
    author='demmonico',
    version='0.7',
    long_description=description,
    long_description_content_type='text/markdown',

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
