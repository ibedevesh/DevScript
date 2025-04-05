from setuptools import setup, find_packages

setup(
    name="devscript",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "python-dotenv",
        "pandas",
        "matplotlib",
        "appdirs",  # For finding config directories
    ],
    entry_points={
        "console_scripts": [
            "devscript=devscript.cli:main",
            "devscript-setup=devscript.setup_cli:main",
        ],
    },
    description="DevScript - AI-powered coding language",
    author="DevScript Team",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/devscript",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    include_package_data=True,
)