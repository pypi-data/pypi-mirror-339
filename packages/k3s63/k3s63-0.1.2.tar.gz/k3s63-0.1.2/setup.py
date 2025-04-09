from setuptools import setup, find_packages

setup(
    name='k3s63',
    version='0.1.2',
    author='@k3s63',
    author_email='k3s63c@gmail.com',
    description='Toolkit by @k3s63 with date and reset functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/k3s63/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
