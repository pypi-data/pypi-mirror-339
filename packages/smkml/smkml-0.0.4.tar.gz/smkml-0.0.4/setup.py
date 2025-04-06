from setuptools import setup, find_packages

setup(
    name="smkml",
    version="0.0.4",
    author="Vansh Gautam",
    author_email="vanshgautam2005@gmail.com",
    description="A hybrid ML algorithm combining SVM and K-Means for classification and clustering.",
    long_description=open("README.md").read(),
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
