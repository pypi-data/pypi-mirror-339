from setuptools import setup, find_packages

setup(
    name="notescli-tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "flask",
        "pymongo"
    ],
    entry_points={
        "console_scripts": [
            "notescli=cli.main:cli"
        ]
    },
    include_package_data=True,
    author="Raaghavi",
    author_email="krraaghavi@example.com",
    description="A CLI Tool for taking notes with Auth0 Security",
    url="https://github.com/Raaghavi-K-R/Notescli",
)
