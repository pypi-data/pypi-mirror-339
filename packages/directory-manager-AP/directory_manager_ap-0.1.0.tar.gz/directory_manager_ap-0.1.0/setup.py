from setuptools import setup, find_packages

setup(
    name="directory-manager-AP",
    version="0.1.0",
    author="Александр",
    author_email="sanyapetrooo@gmail.com",
    description="Универсальный инструмент для работы с директориями и файлами",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(where=".", include=["dir_manager", "dir_manager.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)