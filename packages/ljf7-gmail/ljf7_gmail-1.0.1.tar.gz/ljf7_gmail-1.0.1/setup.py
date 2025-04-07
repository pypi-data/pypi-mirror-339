from setuptools import setup

setup(
    name="ljf7_gmail",
    version="1.0.1",
    description="Math utilities with Fibonacci, factorial, and Gmail email sending functionality.",
    long_description="This module provides simple math functions like Fibonacci and factorial, along with tools for sending emails via Gmail. Ideal for experimenting with basic Python automation.",
    long_description_content_type="text/plain",
    author="Andy Woz",
    py_modules=["ljf7_gmail.math_utils", "ljf7_gmail.spam"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)