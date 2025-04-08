from setuptools import setup, find_packages

setup(
    name="taphealth-kafka",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "kafka-python>=2.0.0",
    ],
    author="Afif",
    author_email="afif@tap.health",
    description="Kafka utilities for TapHealth Python services",
    keywords="kafka, taphealth",
    python_requires=">=3.8",
)
