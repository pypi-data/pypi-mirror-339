from setuptools import setup, find_packages

setup(
    name="smkml",
    version="0.0.9",
    author="Vansh Gautam",
    author_email="vanshgautam2005@gmail.com",
    description="A unified machine learning toolkit for classification, clustering, distance metrics, and model analysis—optimized for both supervised and unsupervised tasks.",
    long_description=open("Readme.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    github="private",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
