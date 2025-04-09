from setuptools import setup, find_packages

setup(
    name="yteva",
    version="2025.4.8",
    packages=find_packages(),
    install_requires=[
        "requests",
        "httpx==0.25.0",
        "pyrofork"
    ],
    author="Eslam",
    author_email="your_email@example.com",
    description="yteva library for downloading audio and videos from YouTube and details about them.",
    url="https://t.me/CH_Twiins",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
