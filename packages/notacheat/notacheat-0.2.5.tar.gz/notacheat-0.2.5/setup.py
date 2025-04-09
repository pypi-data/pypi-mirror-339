import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notacheat",
    version="0.2.5",
    author="Minjae Park 25-21208",
    author_email="minjaepark3837@gmail.com",
    description="A package made so that all hischoolers can use.", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/P-Minjae",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)