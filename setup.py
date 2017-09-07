import os
from setuptools import setup, find_packages
from setuptools.extension import Extension
import sys


try:
    from Cython.Distutils import build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False


cmdclass = {}
long_description=open('README.rst', encoding='utf-8').read()


if USE_CYTHON:
    ext_modules = [
        Extension("dht22.rbp2", ["dht22/rbp2.pyx",
                                 "dht22/common_dht_read.c",
                                 "dht22/pi_2_dht_read.c",
                                 "dht22/pi_2_mmio.c"],
                  extra_compile_args=["-std=c11", "-D_DEFAULT_SOURCE"])
    ]
    cmdclass['build_ext'] = build_ext
else:
    ext_modules = [
        Extension("dht22.rbp2", ["dht22/rbp2.c",
                                 "dht22/common_dht_read.c",
                                 "dht22/pi_2_dht_read.c",
                                 "dht22/pi_2_mmio.c"],
                  extra_compile_args=["-std=c11", "-D_DEFAULT_SOURCE"])
    ]


setup(
    name='dht22',
    version='0.0.1',
    author='Simon Gomizelj',
    author_email='simon@vodik.xyz',
    packages=find_packages(),
    license="Apache 2",
    url='https://github.com/vodik/dht22',
    description='Python3 serializer with memoryview support',
    long_description=long_description,
    install_requires=[
        'aiohttp',
        'aiohttp-index',
        'aiozmq',
        'pandas',
        'msgpack-python',
    ],
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    entry_points={
        'console_scripts': [
            'dht22=dht22.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
