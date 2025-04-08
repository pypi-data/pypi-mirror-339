from setuptools import setup, find_packages

setup(
    name="scematicsapp",
    version=" 0.1.0.dev3",
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "rich",
        "pillow",
        "opencv-python",
        "pathlib",
    ],
    entry_points={
        'console_scripts': [
            'scematicsapp=scematicsapp.cli:main',
        ],
    },
    author="scematics.io",
    author_email="karthickeyan@scematics.xyz",
    description="A CLI tool for managing file uploads",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/scematicsapp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
