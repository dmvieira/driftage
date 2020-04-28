""" Setup script for the driftage library.

"""
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt") as reqs:
    requirements = reqs.read().split("\n")


def main() -> int:
    """ Execute the setup commands.

    """
    setup(
        name = "driftage",
        version = "DYNAMIC",
        url = "https://github.com/dmvieira/driftage",
        author = "Diogo Munaro Vieira",
        author_email = "diogo.mvieira@gmail.com",
        packages = find_packages("driftage"),
        description = "Multi-agent Drift Detection Platform",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        install_requires = requirements,
        license = "Apache 2",
        include_package_data = True,
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Libraries :: Application Frameworks"
        ],
    )
    return 0


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
