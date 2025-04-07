import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bridgepy",
    version="0.0.12",
    author="Papan Yongmalwong",
    author_email="papillonbee@gmail.com",
    description="bridgepy is a python package for playing floating bridge!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/papillonbee/bridgepy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.10',
    install_requires=[
    ],
    keywords=[
        "floating bridge",
        "singaporean bridge",
    ],
)

# pip3 install -e .
# pip3 install setuptools wheel twine
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
