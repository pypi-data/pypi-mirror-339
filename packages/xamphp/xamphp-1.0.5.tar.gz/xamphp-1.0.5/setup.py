from setuptools import setup, find_packages

setup(
    name="xamphp",
    version="1.0.5",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "xamphp=xamphp.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "xamphp": [
            "main.py",
            "__init__.py",
            ".system/imports.py",
            ".system/index.py",
            ".system/modules/localhost.py",
            ".system/sources/clight.json",
            ".system/sources/hosts",
            ".system/sources/logo.ico",
            ".system/sources/vhosts.conf"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="XAMPHP is a command-line interface app designed to launch PHP projects via XAMPP engine from any location on your Windows machine as a virtual local host",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IG-onGit/XAMPHP",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
