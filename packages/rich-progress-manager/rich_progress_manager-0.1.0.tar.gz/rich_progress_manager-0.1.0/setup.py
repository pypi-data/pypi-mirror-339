from setuptools import setup, find_packages

setup(
    name="rich-progress-manager",
    version="0.1.0",
    description="Thread-safe progress manager with rich logging",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/rich-progress",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "typing_extensions; python_version<'3.8'"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="progress logging threading",
)