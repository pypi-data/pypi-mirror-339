from setuptools import setup, find_packages

setup(
    name='axisapi2',
    version='2.0.0',
    description='Axis API 2.0 "Ella" for connecting to a hosted llama instance.',
    author='Wyatt Brashear',
    author_email='wyattb@hackclub.app',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)