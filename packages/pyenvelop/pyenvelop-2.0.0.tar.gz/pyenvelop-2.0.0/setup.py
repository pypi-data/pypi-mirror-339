from setuptools import setup, find_packages

setup(
    name="pyenvelop",
    version="2.0.0",
    description="A Python package for handling envelope-style data structures",
    author="linzhiwei",
    author_email="linzhiwie@foxmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.7",
    license="Proprietary",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Private :: Do Not Upload"
    ],
) 