"""Setup configuration for the IntelliAgent backend package."""

from setuptools import find_packages, setup

setup(
    name="intelliagent-backend",
    version="0.1.0",
    packages=find_packages(),
    # This allows for an editable install
    # `pip install -e .`
)
