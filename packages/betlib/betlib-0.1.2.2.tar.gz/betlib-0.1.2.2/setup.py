from setuptools import find_packages, setup

setup(
    name="betlib",
    version="0.1.2.2",
    author="Pierre Peigné",
    description="Minimalist Library for calling PRISM Eval BET API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "requests",
        "aiohttp",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest"
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)