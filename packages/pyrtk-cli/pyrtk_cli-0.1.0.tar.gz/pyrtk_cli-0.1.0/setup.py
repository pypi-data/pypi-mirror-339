from setuptools import setup, find_packages

setup(
    name="pyrtk-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "fastapi",
        "uvicorn",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "pyrtk=pyrtk.cli:main",
        ],
    },
    author="Andres Mardones",
    description="Python REST Toolkit CLI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)