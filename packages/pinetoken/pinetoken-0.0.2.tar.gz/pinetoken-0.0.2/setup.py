from setuptools import setup, find_packages

setup(
    name="pinetoken",
    version="0.0.1",
    description="A secure and simple CLI token manager with encryption support.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="openpineaplehub",
    author_email="openpineaple@gmail.com",
    url="https://github.com/openpineapletools/pinetoken",
    project_urls={
        "Homepage": "https://github.com/openpineapletools/pinetoken",
        "Repository": "https://github.com/openpineapletools/pinetoken",
        "Issues": "https://github.com/openpineapletools/pinetoken/issues",
    },
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "cryptography>=41.0.3",
        "tabulate>=0.9.0"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pinetoken=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
    keywords=["CLI", "token", "manager", "security", "encryption", "password"],
)
