from setuptools import setup, find_packages

setup(
    name="sas_comm_py",
    version="0.1.0",
    description="Python library to communicate with slot machines using serial port",
    author="Mayled",
    author_email="mayleddev88@gmail.com",
    url="https://github.com/mdedz/sas_comm_py",
    packages=find_packages(),
    install_requires=[
        "pyserial",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
