from setuptools import setup, find_packages

setup(
    name="cffsdk",
    version="0.1.1",
    description="A Python client for interacting with CFF server.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aalap Tripathy",
    author_email="aalap.tripathy@hpe.com",
    url="https://github.com/atripathy86/cff",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)