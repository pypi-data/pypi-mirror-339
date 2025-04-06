from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="silentis-ai",
    version="1.1.7",
    author="Silentis Team",
    author_email="support@silentis.ai",
    description="Silentis AI - A powerful AI assistant plugin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Silentisai/Silentis",
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version required
    install_requires=[
        "flask",
        "requests",
        "llama-cpp-python",
        "psutil",
        "flask-cors",
    ],  # Add all dependencies here
    include_package_data=True,  # Include non-Python files (e.g., config.json)
    entry_points={
        "console_scripts": [
            "silentis=silentisai.run:main",  # Allows running as `silentis` command
        ],
    },
)



