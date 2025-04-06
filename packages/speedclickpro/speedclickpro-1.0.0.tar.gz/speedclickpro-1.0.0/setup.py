from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="speedclickpro",
    version="1.0.0",
    author="SpeedClick Pro Team",
    author_email="your.email@example.com",  # Change this to your email
    description="Advanced auto-clicker with animation sequencing capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/speedclickpro",  # Change to your repo if any
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/speedclickpro/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
        "Intended Audience :: End Users/Desktop",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "speedclickpro": ["icons/*", "profiles/*"],
    },
    python_requires=">=3.7",
    install_requires=[
        "pyautogui>=0.9.54",
        "keyboard>=0.13.5",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "speedclickpro=speedclickpro:main",
        ],
    },
)
