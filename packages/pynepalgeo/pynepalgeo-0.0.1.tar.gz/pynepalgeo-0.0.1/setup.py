from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pynepalgeo",  # Package name
    version="0.0.1",  # Initial version
    author="Mahesh Acharya",  # Replace with your name
    author_email="mahesh01acharya@gmail.com",  # Replace with your email
    description="A Python package to get information about provinces, districts, and municipalities of Nepal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smaheshacharya/nepal-geo-info",  # Replace with the actual URL of your project
    packages=find_packages(),  # Automatically find all packages in your directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Use the appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[  # List any dependencies your package needs
        # Example: "requests", "pandas"
    ],
    include_package_data=True,  # Include non-code files listed in MANIFEST.in
      package_data={
        'pynepalgeo': [
            'dataset/provinces/en.json',
            'dataset/districts/en.json',
            'dataset/municipalities/en.json',
            'dataset/alldataset/en.json'
        ],
    },
 
)
