from setuptools import setup, find_packages

setup(
    name="Mechalyze",  # Package name
    version="0.1.0a1",  # Initial version
    author="Mohnish S",
    author_email="mohnishs2006@gmail.com",
    description="A mechanical engineering analysis package, which has tools for plotting values also uses stastical and historical analysis to give more precise answer.",
    long_description=open("README.md").read(),  # If you have a README.md
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mechalyse",  # Replace with your actual repo (if any)
    packages=find_packages(),  # Automatically finds all packages
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
