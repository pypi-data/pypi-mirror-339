from setuptools import setup, find_packages

setup(
    name="pepsales_retry_lib",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "kafka-python>=2.0.2",
        "requests>=2.31.0",
        "pymongo>=3.10.1",
        "confluent-kafka>=2.3.0",
        "datetime"
    ],
    author="Pepsales",
    author_email="abhinandan@pepsales.ai",
    description="A Kafka-based retry mechanism for API requests with success/failure callbacks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
