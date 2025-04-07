from setuptools import setup, find_packages

setup(
    name='easyconvert',
    version='0.1.0',
    author='Rafsan',
    description='A simple unit conversion library for Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/easyconvert',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
