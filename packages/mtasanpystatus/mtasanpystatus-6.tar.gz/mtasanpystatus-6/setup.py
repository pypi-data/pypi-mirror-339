from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mtasanpystatus",
    version="6",
    author="ieoub",
    author_email="rib7daily@gmail.com",
    description="Multi Theft Auto San Andreas Server Monitoring Library Using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ieoub/mtasanpystatus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'twine>=3.0',
        ],
    },
)