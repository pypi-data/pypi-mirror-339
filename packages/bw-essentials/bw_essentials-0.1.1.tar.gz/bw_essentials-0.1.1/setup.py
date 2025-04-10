from setuptools import setup, find_packages

setup(
    name="bw-essentials",
    version="0.1.1",
    author="Your Name",
    author_email="you@example.com",
    description="Reusable utilities for S3, email, Data Loch, encryption, and more",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
