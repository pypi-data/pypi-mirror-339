from setuptools import setup, find_packages

setup(
    name="smolbox",
    version="0.0.0",
    author="You",
    author_email="you@example.com",
    description="A tiny dummy package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
