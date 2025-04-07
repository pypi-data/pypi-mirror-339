from setuptools import setup, find_packages

setup(
    name="openscan",
    version="0.1.0",
    author="Mr.Balakavi",
    author_email="balakavi64@gmail.com",
    description="A simple Python package to scan open ports on an IP address",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mr-bala-kavi/openscan",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)