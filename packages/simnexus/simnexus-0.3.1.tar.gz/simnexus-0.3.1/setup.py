from setuptools import setup, find_packages

setup(
    name="simnexus",
    version="0.3.1",
    author="Michael",
    description="DEPRECATED: Please use sim-lab instead",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michael/simnexus",
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        "sim-lab>=0.3.0",
    ],
    classifiers=[
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)