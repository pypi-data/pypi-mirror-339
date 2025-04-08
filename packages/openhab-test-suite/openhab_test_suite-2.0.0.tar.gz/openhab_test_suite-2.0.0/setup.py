from setuptools import setup, find_packages

setup(
    name='openhab-test-suite',
    version='2.0.0',
    author='Michael Christian Dörflinger',
    author_email='michaeldoerflinger93@gmail.com',
    description='A comprehensive testing library for validating and interacting with openHAB installations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Michdo93/openhab-test-suite',
    packages=find_packages(),
    install_requires=[
        'python-openhab-rest-client',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
