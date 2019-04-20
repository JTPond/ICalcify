import setuptools

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
    name="icalcify-jtpond42",
    version="0.0.1",
    author="Josh Pond",
    author_email="jtpond42@gmail.com",
    description="Interactive analysis tool for Calcify Trees.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JTPond/ICalcify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
)
