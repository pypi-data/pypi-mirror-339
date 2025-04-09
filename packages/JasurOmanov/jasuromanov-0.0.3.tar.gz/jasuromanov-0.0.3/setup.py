from setuptools import setup, find_packages

setup(
    name='JasurOmanov',  # PyPI dagi nomi
    version='0.0.3',
    description='Oddiy kutubxona',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jasur Omanov',
    author_email='jasuromanov05@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
