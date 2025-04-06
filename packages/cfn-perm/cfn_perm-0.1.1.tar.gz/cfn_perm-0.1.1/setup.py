from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="cfn-perm",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "boto3",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "cfn-perm=source.app:main",
        ],
    },
    author="S Murali Krishnan",
    author_email="mrlikrsh@gmail.com",
    description="A tool to automatically generate IAM permissions from CloudFormation templates",
    keywords="aws, cloudformation, iam, permissions",
    url="https://github.com/mrlikl/cfn-perm.git",
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
)
