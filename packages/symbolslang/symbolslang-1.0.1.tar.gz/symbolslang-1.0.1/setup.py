from setuptools import setup, find_packages

setup(
    name="symbolslang",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "symbols=symbols.__init__:main",  # Register the 'symbols' command
        ],
    },
    install_requires=[],  # Add dependencies here if needed
    description="A CLI tool for compiling and executing symbols.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/symbols",  # Replace with your GitHub repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
