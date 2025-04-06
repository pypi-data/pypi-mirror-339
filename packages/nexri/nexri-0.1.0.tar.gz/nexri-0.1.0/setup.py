from setuptools import setup, find_packages

# Read the contents of README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nexri",
    version="0.1.0",
    author="Pawel Tomkiewicz",
    author_email="pawel.tomkiewicz@nexri.eu",
    description="Advanced layers for TensorFlow Keras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexri/nexri",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "tensorflow>=2.19.0",
    ],
)
