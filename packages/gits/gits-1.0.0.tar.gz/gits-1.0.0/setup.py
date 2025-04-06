from setuptools import setup, find_packages

setup(
    name="gits",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "gits=gits.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "gits": [
            "main.py",
            "__init__.py",
            ".system/imports.py",
            ".system/index.py",
            ".system/modules/jobs.py",
            ".system/sources/clight.json",
            ".system/sources/logo.ico"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="Gits is a Python command-line application designed to help you manage multiple GitHub and GitLab repositories on your development machine. Using it, you can easily generate a new SSH key and add a new account to the list with just one command. After that, you can start cloning from and pushing to multiple GitHub and GitLab accounts without any additional OS or HTTP-level configurations. It automatically sets up everything needed to prevent conflicts between your repositories and accounts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IG-onGit/Gits",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
