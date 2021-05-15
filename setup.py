import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
    version="0.0.1",
    author="Rabiul Islam",
    author_email="author@example.com",
    description="A small package for converting Bijoy characters to Unicode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rabiulislam-xyz/bijoy-to-unicode-converter-python",
    project_urls={
        "Bug Tracker": "https://github.com/rabiulislam-xyz/bijoy-to-unicode-converter-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)