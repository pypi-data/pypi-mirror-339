from setuptools import setup, find_packages

setup(
    name="OmSatyawanPathak",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["matplotlib"],  # Dependency
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple plotting library for Python programmers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/OmSatyawanPathak",  # Optional GitHub link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)