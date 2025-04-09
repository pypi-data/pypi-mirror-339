import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotstxt",
    version="1.1.2",
    author="Christopher Evans",
    author_email="chris@chris24.co.uk",
    description="A Python package to check URL paths against robots directives a robots.txt file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisevans77/robotstxt_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)