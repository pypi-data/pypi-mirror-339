from setuptools import setup, find_packages


# read the contents of the README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="magicode",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "click",
        "keyring",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'magicode=magicode.main:cli',  # Changed from main to cli
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
