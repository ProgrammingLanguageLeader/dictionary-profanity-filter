from setuptools import setup, find_packages

print(open('README.md').read().strip())

setup(
    name='dictionary-profanity-filter',
    version=open('VERSION').read().strip(),
    license='MIT license',
    author='Dmitry Shorokhov',
    author_email='vip.shoroch@gmail.com',
    description='Python profanity filter',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'dictionary-profanity-filter = '
                'dictionary_profanity_filter.__main__:main',
        ]
    }
)
