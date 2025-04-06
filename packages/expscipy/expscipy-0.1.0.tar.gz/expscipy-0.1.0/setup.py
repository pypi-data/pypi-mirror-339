import os
from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read version from version.py
about = {}
with open(os.path.join('src', 'expscipy', 'version.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name='expscipy',
    version=about['__version__'],
    author='Sumedh Patil',
    author_email='sumedh@aipresso.com',
    description='Enhanced version of SciPy with additional scientific computing features',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Sumedh1599/expscipy',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=[
        'scipy>=1.0.0',
        'numpy>=1.20.0',
        'scipy>=1.7.0'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'isort>=5.0.0',
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Sumedh1599/expscipy/issues',
        'Source': 'https://github.com/Sumedh1599/expscipy',
        'Documentation': 'https://expscipy.readthedocs.io/',
    },
)
