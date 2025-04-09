from setuptools import setup, find_packages

setup(
    name="minisecret",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["cryptography"],
    entry_points={
        "console_scripts": [
            "minisecret=minisecret.__main__:main",
        ],
    },
    author="Lars Söderblom",
    author_email="",
    description="A minimal AES-256-GCM-based secrets manager for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Cognet-74/MiniSecret",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)