from setuptools import setup, find_packages

setup(
    name="pyillustrator",  # Replace with your module name
    version="0.9.0",
    author="Isaac",
    author_email="isaac.robledo.martin@gmail.com",
    description="A Python module for generating various plots using Matplotlib",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ipatazas/pyillustrator",  # Replace with your GitHub repo
    packages=find_packages(),  # Automatically finds all packages in the module
    package_dir={"": "."},
    install_requires=[
        "matplotlib>=3.0.0",
        "numpy>=1.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
