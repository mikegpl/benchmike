from setuptools import setup

setup(
    name='benchmike',
    version='1.0',
    description='Module for measuring time complexity of functions',
    license='MIT',
    url='www.github.com/mikegpl',
    author='Michał Grabowski',
    author_email='mkg.grabowski@gmail.com',
    packages=['benchmike'],
    install_requires=['numpy', 'argparse', 'matplotlib'],
    entry_points={
        'console_scripts': [
            'benchmike = benchmike.benchmike:main'
        ]
    }

)
