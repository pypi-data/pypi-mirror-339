from setuptools import setup, find_packages
import os

# Read the README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="codesnapper",
    version="0.1.5", # Incremented version after package restructure
    author="CodeSnapper Contributors",
    author_email="your.email@example.com",  # Replace with your email
    description="A tool to create code snapshots by combining multiple files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/codesnapper",  # Replace with your repo URL
    packages=find_packages(), # Find packages automatically (like 'codesnapper')
    include_package_data=True, # Include files specified in MANIFEST.in
    install_requires=[
        "colorama>=0.4.6",
        "pyperclip>=1.8.2",
        "Flask>=2.0", # Added Flask
        "psutil>=5.9.0" # Added for single-instance check
    ],
    entry_points={
        'console_scripts': [
            'codesnap=codesnapper.app:start_server', # Updated path for entry point
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
