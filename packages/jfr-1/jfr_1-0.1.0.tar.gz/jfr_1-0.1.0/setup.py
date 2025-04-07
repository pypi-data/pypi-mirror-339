from setuptools import setup, find_packages

setup(
    name="jfr_1",  # Change this to your package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    author="Jaafari Anass",
    author_email="anassjaafari.aj@gmail.com",
    description="A simple test library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jfr_1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
