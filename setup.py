from setuptools import find_packages, setup

setup(
    name='brr',
    packages=find_packages(),
    version='0.1.0',
    description='Python pachage to collected data from freezing experiments to estimate INP concentration as function of the activation temperature in the immersion freezing mode.',
    author='gfogwill',
    license='MIT',
    entry_points={"console_scripts": ["brr = brr.cli:cli"]},
)
