from setuptools import setup, find_packages

setup(
    name="promptshieldhoohacks",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="promptShield",
    description="Python SDK for the PromptShield AI firewall API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/you/promptshield-sdk",
)