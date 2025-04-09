from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stack-upgrade-analyzer",
    version="0.1.1",
    author="Trilogy Group",
    author_email="info@trilogy.com",
    description="A tool for analyzing code compatibility issues when upgrading technology stacks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trilogy-group/upgrade-analyzer",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click",
        "boto3",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "stack-upgrade-analyzer=stack_upgrade_analyzer.cli:main",
        ],
    },
)
