from setuptools import setup, find_packages

setup(
    name="MDATP",
    version="0.0.1",
    description="Microsoft Defender Advanced Threat Protection SDK for Python 3.6",
    author="sebastian",
    author_email="seba@cloudnative.co.jp",
    packages=find_packages(),
    install_requires=[
        "jsonschema"
    ],
    entry_points={
        "console_scripts": [
        ]
    },
)
