from setuptools import setup, find_packages
import codecs
import os

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = "0.0.7"
DESCRIPTION = "Flask HTTP Middleware with starlette's (FastAPI) BaseHTTPMiddleware style"

# Setting up
setup(
    name="flask-http-middleware",
    version=VERSION,
    author="danangjoyoo (Agus Danangjoyo)",
    author_email="<agus.danangjoyo.blog@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["flask","werkzeug","asgiref"],
    keywords=['flask', 'middleware', 'http', 'request', "response"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Typing :: Typed"
    ]
)