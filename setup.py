from pip.req import parse_requirements
from setuptools import setup, find_packages

version = open('VERSION').read().strip()
license = open('LICENSE').read().strip()

setup(
    name='dictionary-profanity-filter',
    version=version,
    license=license,
    author='Dmitry Shorokhov',
    author_email='vip.shoroch@gmail.com',
    description='Python profanity filter',
    long_description=open('README.md').read().strip(),
    packages=find_packages(),
    install_requires=[
        parse_requirements('requirements.txt')
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'dictionary-profanity-filter = '
            'dictionary-profanity-filter.__main__:main',
        ]
    }
)
