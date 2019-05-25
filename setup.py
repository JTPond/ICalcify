import setuptools

with open("README.md","r") as f:
    long_description = f.read()

with open("LICENSE","r") as f:
    license = f.read()

setuptools.setup(
    name="icalcify-jtpond42",
    version="0.0.25",
    author="Josh Pond",
    author_email="jtpond42@gmail.com",
    description="Interactive analysis tool for Calcify Trees.",
    long_description=long_description,
    url="https://github.com/JTPond/ICalcify",
    license=license,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
                  'numpy',
                  'scipy',
                  'matplotlib',
                        ],
    entry_points = {'console_scripts':['icalcify=ICalcify.command_line:main'],}
)
