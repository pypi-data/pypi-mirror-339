from setuptools import setup, find_packages

setup(
    name="PyZest",          # Name on PyPI 
    version="0.1.0",             # Version
    packages=find_packages(),    # Find
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "aiogram>=2.23.1",
        "tqdm>=4.60.0",
        "PySide6>=6.4.0"
    ],         # Needing 
    author="RedFlyMeer",
    author_email="redflymeer@gmail.com",
    description="Easy Python Tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/redflymeer/PyZest",
    keywords="python easy http gui telegram web files",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",     # Минимальная версия Python
)
