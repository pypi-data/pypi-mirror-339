from setuptools import setup, find_packages

setup(
    name="necmec_api",
    version="0.1.0",
    author="Bipul Kumar Kuri",
    description="Python client for interacting with the necmec API",  # Short description
    url="https://github.com/bipulkkuri/necmec_api",
    packages=find_packages(),
    # Keywords:
    TAGS = [
    "utilities",
    "api",
    "necmec"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[
        "requests>=2.25.1"
    ],
    entry_points={
        'console_scripts': [
            'necmec-cli=necmec_api.cli:main',
        ],
    },
)
