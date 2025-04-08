import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pnne_search",
    version="0.1.1",
    # author="Your Name",
    # author_email="your.email@example.com",
    description="A package for search model estimation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pnnehome.github.io/",
    packages=setuptools.find_packages(),
    include_package_data=True,  
    install_requires=[
        "tensorflow>=2.0.0", 
        "numpy>=1.15",  
        "scipy>=1.0.0", 
        "pandas>=1.0.0",
        "joblib>=0.14.0",
        "absl-py>=0.13.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
