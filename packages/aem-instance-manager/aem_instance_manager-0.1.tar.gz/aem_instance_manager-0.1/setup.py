from setuptools import setup, find_packages

setup(
    name="aem_instance_manager",
    version="0.1",
    author="Mayur Satav",
    author_email="mayursatav9@gmail.com",
    description="An AEM instance management tool designed to simplify switching across multiple project environments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mayursatav/aem-instance-manager",
    packages=find_packages(),
    install_requires=[
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "aem-instance-manager = aem_instance_manager.main:main",
        ],
    },
)
