from setuptools import setup, find_packages

setup(
    name="GetLatestGamePrices",           
    version="0.2.0",            
    description="This Package gets you the deals about a single game from ggdeals. also this is my first package to learn about things like packages, version control, github actions",
    author="AbhayCerberus",
    author_email="mistercerberus01+pypiPackage@gmail.com",
    packages=find_packages(),   
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    url="https://github.com/Abhay_Cerberus/GetLatestGamePrices"
)