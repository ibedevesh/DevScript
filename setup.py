from setuptools import setup, find_packages

setup(
    name="devscript-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "devscript=devscript_client:main",
        ],
    },
    description="DevScript client - AI-powered coding language",
    author="DevScript Team",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/devscript-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)