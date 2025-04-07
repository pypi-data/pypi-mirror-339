from setuptools import setup

setup(
    name="spam7",
    version="1.0.1",
    description="Python module calling",
    long_description="Tools for sending emails via Gmail. Ideal for experimenting with basic Python automation.",
    long_description_content_type="text/plain",
    author="Andy Woz",
    py_modules=["spam7"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)