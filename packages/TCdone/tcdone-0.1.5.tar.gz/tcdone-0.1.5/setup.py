from setuptools import setup, find_packages

setup(
    name="TCdone",
    version="0.1.5",
    description="A Python package to download and manage tropical cyclone datasets like IBTrACS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cong Gao",
    author_email="cong.gao@princeton.edu",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
