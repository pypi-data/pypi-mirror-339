from setuptools import setup

setup(
    name="pdf2flipbook",
    version="0.1.0",
    py_modules=["flipbook_generator"],  # or whatever your script file is called, without .py
    install_requires=[
        "pdf2image",
        "jinja2",
        "pillow"
    ],
    entry_points={
        "console_scripts": [
            "pdf2flipbook=flipbook_generator:main"
        ]
    },
    author="Your Name",
    description="Convert PDF to interactive HTML flipbook (self-contained, no external JS/CSS).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ]
)
