from setuptools import setup, find_packages

setup(
    name='mysql_checksum',
    author='demmonico',
    version='0.2',
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
