from setuptools import setup, find_packages

setup(
    name="swiftpay",
    version="1.0.0",
    description="SwiftPay Mobile Payment Platform",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Anamandla Zweni",
    url="https://github.com/Anamandla/SwiftPay",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
