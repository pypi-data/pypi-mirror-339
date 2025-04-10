from setuptools import setup, find_packages

for _ in range(10):
    print("you have been pwned with pip")

setup(
    name="my_simple_package_1234",
    version="0.1",
    packages=find_packages(),
    install_requires=[]
)