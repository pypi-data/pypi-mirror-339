import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anzu",
    version="0.1.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for updating queue items in a Django service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/queue_updater",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.7.3",
        "python-socketio>=5.12.1",
    ],
)