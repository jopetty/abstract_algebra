from setuptools import setup

setup(
    name='abstract_algebra',
    version='0.0.2',
    package_dir={"abstract_algebra": "src"},
    packages=['abstract_algebra'],
    url='https://abstract-algebra.readthedocs.io/en/latest/index.html',
    license='MIT',
    author='Alfred J. Reich',
    author_email='al.reich@gmail.com',
    description='A Python implementation of Finite Algebras: Magma, Semigroup, Monoid, Group, Ring, and Field'
)
