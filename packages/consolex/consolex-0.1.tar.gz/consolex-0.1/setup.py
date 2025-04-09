from setuptools import setup, find_packages

setup(
    name='consolex',
    version='0.1',
    packages=find_packages(),
    description='A modern console logging module for Python but similar JavaScript',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Əli Zülbalayev',
    author_email='pulixbot@gmail.com',
    url='https://github.com/shadowchaser/consolepy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
