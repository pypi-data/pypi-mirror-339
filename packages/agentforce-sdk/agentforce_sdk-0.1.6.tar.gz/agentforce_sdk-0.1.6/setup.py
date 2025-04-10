from setuptools import setup, find_packages
import os

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read LICENSE file
with open("LICENSE", "r", encoding="utf-8") as f:
    license_text = f.read()

# Get version from package
version = "0.1.0"
with open(os.path.join("agent_sdk", "__init__.py"), "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("'").strip('"')
            break

setup(
    name="agentforce-sdk",
    version=version,
    author="Salesforce",
    author_email="agentforce@salesforce.com",
    description="Python SDK for creating, managing, and deploying AI agents in Salesforce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/agent-sdk",
    packages=find_packages(exclude=["tests*"]),
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.0.0",
        "requests>=2.28.0",
        "simple-salesforce>=1.12.0",
        "openai>=1.0.0",
    ],
    include_package_data=True,
    package_data={
        "agent_sdk": ["core/templates/**/*"],
    },
    entry_points={
        'console_scripts': [
            'agentforce-server=agent_sdk.server:main',
        ],
    },
) 