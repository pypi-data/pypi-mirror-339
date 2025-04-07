from setuptools import setup, find_packages


setup(
    name="polycconsmath",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[],
    author="Constantina",
    author_email="polyccon@gmail.com",
    description="A simple math operations package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/polyccon/python-packages",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.11",
)