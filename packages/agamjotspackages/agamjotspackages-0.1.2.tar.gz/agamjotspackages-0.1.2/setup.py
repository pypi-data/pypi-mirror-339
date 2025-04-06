from setuptools import setup, find_packages

setup(
    name='agamjotspackages',
    version='0.1.2',
    author='Agamjot',
    author_email='agamjotlamba55@gmail.com',
    description='A collection of Python packages for various utilities and functionalities.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'cohere',
    ],
)


