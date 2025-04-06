# setup.py

from setuptools import setup, find_packages

setup(
    name="mll1416",  # or whatever new unique name you choose,  # This is your module name
    version="0.1.0",
    author="Peter1416",
    author_email="your_email@example.com",
    description="A minimal module named mll for Python utilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mll",  # Optional: your repo
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
