from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "An OpenAPI documentation generator for Flask"
LONG_DESCRIPTION = "Flask-Swadantic is a library to generate OpenAPI documentation automatically from Flask applications."

# Setting up
setup(
    name="flask-swadantic",
    version=VERSION,
    author="Lucas de Freitas Ponick",
    author_email="<lucas_ponick@hotmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "flask=>=3.1.0,<4.0.0",
        "pydantic=>=2.10.5,<3.0.0",
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    python_requires=">=3.10",
    keywords=["python", "first package"],
    classifiers=[
        "Topic :: Software Development :: Documentation",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
)
