from setuptools import setup, find_packages

setup(
    name='Tams',
    version='1.0.0',
    description='Package matematika sederhana',
    author='Arya Wiratama',
    author_email='aryawiratama2401@gmail.com',
    package_data={"Tams": ["*.py"]},
    python_requires='>=3.10',
    packages=find_packages()
)