from setuptools import setup

setup(
    name="devscript-client",
    version="0.1.0",
    py_modules=["devscript_client"],  # Use py_modules instead of find_packages
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
    url="https://github.com/ibedevesh/DevScript",  # Updated to your actual GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
