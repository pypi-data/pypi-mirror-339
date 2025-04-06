from setuptools import setup, find_packages

setup(
    name="docbuddy",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "ask-docs>=0.1.0",
    ],
    description="Deprecated: Use ask-docs instead",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/docbuddy",
    classifiers=[
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)