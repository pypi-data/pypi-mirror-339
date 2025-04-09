import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="openrgb-python-ng",
    version='0.3.3',
    author="epulidogil",
    description="A python client for the OpenRGB SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emiliopg91/openrgb-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
