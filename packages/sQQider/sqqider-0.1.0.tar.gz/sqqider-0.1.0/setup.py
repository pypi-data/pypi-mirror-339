from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Define the Cython extensions
extensions = [
    Extension("sQQideR.DatabaseContext", ["sQQideR/DatabaseContext.pyx"]),
    Extension("sQQideR.QueryHistory", ["sQQideR/QueryHistory.pyx"]),
    Extension("sQQideR.SQLBuilder", ["sQQideR/SQLBuilder.pyx"]),
]

# Setup configuration
setup(
    name="sQQider",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Cythonized package for sQQider",
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
    packages=["sQQideR"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)