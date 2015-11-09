from distutils.core import setup

setup(
    name = 'uchicagoSIPS',
    version = '1.0.0',
    author = "Tyler Danstrom",
    author_email = "tdanstrom@uchicago.edu",
    packages = ['uchicagoldrsips'],
    description = """\
    A set of base classes for interacting with University of Chicago library 
    digital repository objects
    """,
    keywords = ["uchicago","repository","file-level","sips"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    install_requires = ['python-magic == 0.4.6'])
