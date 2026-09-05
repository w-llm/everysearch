from setuptools import setup, find_packages

setup(
    name="everysearch",
    version="0.2.0",
    description="A fast, global file/directory search CLI tool with social media username lookup.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/w-llm/everysearch",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "everysearch=everysearch.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
