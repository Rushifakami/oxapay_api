import setuptools
from setuptools import setup, find_packages

setup(
    name='oxapay_api',
    version='1.0.2',
    author='Rushifakami',
    description='Unofficial library for interacting with the OxaPay API. See github for more info: https://github.com/Rushifakami/oxapay_api',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'requests',
        'urllib3'
    ],
    python_requires='>=3.6',
    url='https://github.com/Rushifakami/oxapay_api',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords=[
        'crypto',
        'oxapay',
        'gateway',
        'payment',
        'api'
    ]
)