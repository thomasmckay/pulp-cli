from setuptools import setup, find_packages

setup(
    name="pulpcli",
    version="0.0.1a1",
    url="http://github.com/werwty/pulpcli/",
    description="POC CLI for Pulp",
    author="",
    author_email="",
    packages=find_packages(exclude=["test"]),
    install_requires=["coreapi", "click", "psutil", "progress"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["pulp=pulpcli.main:client"]},
)
