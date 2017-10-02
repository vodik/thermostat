from setuptools import setup, find_packages


long_description=open('README.rst', encoding='utf-8').read()


setup(
    name='sensord',
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
        'msgpack-python',
        'prometheus-async',
        'prometheus-client',
        'pyzmq>=17.0.0b1'
    ],
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
