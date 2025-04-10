from setuptools import setup, find_packages

setup(
    name="beautified",
    version="1.0.0",
    description="A package for CLI text stylization.",
    author="Chase Galloway",
    author_email="chase.h.galloway21@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
    ],
    python_requires=">=3.6",
)
