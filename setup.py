import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graphotti",
    version="0.0.1a1",
    author="Ronny Restrepo",
    author_email="ronny.coding@gmail.com",
    description="A mashable plotting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronrest/graphotti",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
