from setuptools import setup, find_packages

setup(
    name="kaf_retry_wrapper",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "kafka-python>=2.0.2",
        "requests>=2.32.3",
        "pymongo>=4.10.1",
    ],
    author="Anas Iqbal",
    author_email="anas.iqbal@pepsales.ai",
    description="A Kafka-based retry mechanism for API requests with success/failure callbacks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kafka-retry-wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
