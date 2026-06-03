from setuptools import setup, find_packages
setup(
    name="swiftpay",
    version="1.0.0",
    description="SwiftPay Mobile Payment Platform",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
)
