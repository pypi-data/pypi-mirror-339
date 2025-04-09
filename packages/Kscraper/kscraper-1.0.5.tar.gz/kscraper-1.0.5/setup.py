from setuptools import setup, find_packages

setup(
    name="Kscraper",
    version="1.0.5",
    author="chard",
    author_email="chard@azr.tools",
    description="A Python package to bypass cloudflare on kick.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chardWTF/Kscraper",
    packages=find_packages(),
    install_requires=[
        "tls_client",
        "requests",
        "colorama"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
