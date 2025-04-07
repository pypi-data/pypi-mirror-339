from setuptools import setup, find_packages

setup(
    name="stockmanage-lib",
    version="0.1.0",
    author="Neeraj Reddy",
    author_email="pneerajreddy390@gmail.com",
    description="A Django library for stock management with role-based access",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['django>=3.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)