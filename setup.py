from setuptools import setup, find_packages

setup(
    name="marshmallow-pynamodb",
    version="0.8.1",
    packages=find_packages(exclude=("*test*",)),
    package_dir={"marshmallow-pynamodb": "marshmallow_pynamodb"},
    description="PynamoDB integration with the marshmallow (de)serialization library",
    author="Mathew Marcus",
    author_email="mathewmarcus456@gmail.com",
    long_description=open("README.rst").read(),
    install_requires=["marshmallow>=3.0.0", "pynamodb>=4.0.0",],
)
