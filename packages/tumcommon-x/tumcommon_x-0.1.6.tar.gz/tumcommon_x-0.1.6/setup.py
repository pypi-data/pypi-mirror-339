from setuptools import setup, find_packages

setup(
    name="tumcommon-x",
    version="0.1.6",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=5.2",
    ],
    author="TUM Common X Team",
    author_email="burak.sen@tum.de",
    description="A Django package providing common functionality for TUM projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tum-common-x",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
    ],
    python_requires=">=3.8",
) 