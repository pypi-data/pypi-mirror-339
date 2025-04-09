import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="necmec_api",
    version="0.1.2",
    author="Bipul Kumar Kuri",
    description="Python client for interacting with the necmec API",  # Short description
	long_description = README,
	long_description_content_type = "text/markdown",
    url="https://github.com/bipulkkuri/necmec_api",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",  # License type
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
