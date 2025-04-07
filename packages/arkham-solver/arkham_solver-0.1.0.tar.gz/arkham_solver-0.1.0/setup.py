from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="arkham-solver",
    version="0.1.0",
    description="Python client for Arkham Captcha Solver API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arkham Solver",
    author_email="admin@arkham-solver.com",
    url="https://github.com/arkhamsolver/arkham-solver",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="captcha, solver, arkham, api-client",
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3.7, <4",
    install_requires=[
        "requests>=2.25.1",
        "pydantic>=1.8.2",
    ],
    project_urls={
        "Bug Reports": "https://github.com/arkhamsolver/arkham-solver/issues",
        "Source": "https://github.com/arkhamsolver/arkham-solver",
    },
    package_data={
        "arkham_solver": ["py.typed"],
    },
)
