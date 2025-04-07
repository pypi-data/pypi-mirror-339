# setup.py
from setuptools import setup, find_packages

setup(
    name="nutrition-tracker-lib",  # Unique name (check PyPI availability)
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "django>=3.0"
    ],
    author="Your Name",
    author_email="akhilareddykandadi@gmail.com",
    description="A library for tracking nutrition data using the USDA API",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose a license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)