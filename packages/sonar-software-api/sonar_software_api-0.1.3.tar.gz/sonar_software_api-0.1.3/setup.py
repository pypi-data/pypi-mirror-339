from setuptools import setup, find_packages

setup(
    name="sonar_software_api",
    version="0.1.3",
    description="A simple GraphQL client for interacting with your Sonar Software instance",
    author="JckHamm3r",
    packages=find_packages(),
    install_requires=[
        "gql>=3.4.0",
        "requests_toolbelt>=1.0.0"
    ],
    python_requires=">=3.7",
)
