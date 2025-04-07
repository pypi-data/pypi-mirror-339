from setuptools import setup, find_packages

# Read version from your module
version = {}
with open("subdomain_permut/__version__.py") as f:
    exec(f.read(), version)

setup(
    name='subdomain-permut',
    version=version["__version__"],
    author='Shriyans Sudhi',
    author_email='shriyanss@ss0x00.com',
    description='A tool for generating subdomain permutations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shriyanss/subdomain-permut',
    packages=find_packages(),
    install_requires=['argparse'],
    entry_points={
        'console_scripts': [
            'subdomain-permut=subdomain_permut.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)