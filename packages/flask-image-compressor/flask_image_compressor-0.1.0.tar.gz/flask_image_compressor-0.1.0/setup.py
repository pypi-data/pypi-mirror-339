from setuptools import setup, find_packages

setup(
    name="flask-image-compressor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "werkzeug",
        "pillow",
    ],
    author="gnubyte",
    author_email="gnubyte@users.noreply.github.com",
    description="A Flask extension for automatic image compression and optimization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gnubyte/flask-image-compressor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 