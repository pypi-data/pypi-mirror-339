from setuptools import setup, find_packages

setup(
    name="qos-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "websockets>=10.0",
        "pydantic>=1.8.0"
    ],
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="Official Python SDK for QOS Market Data API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qos-api-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)