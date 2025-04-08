from setuptools import setup, find_packages

setup(
    name="smuxent",
    version="0.0.1",
    description="Native threading for Python using C++ and pybind11",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Patryk Wrzesniewski",
    license="MIT",
    packages=["smuxent"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.12,<3.13",
)
