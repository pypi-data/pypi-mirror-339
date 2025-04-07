from setuptools import setup, find_packages

setup(
    name='akm',
    version='1.3.1',
    description='A library for generating and checking temporary Gmail emails.',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'gen-gmail=akm.akm:gen',
            'check-gmail=akm.akm:check',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
