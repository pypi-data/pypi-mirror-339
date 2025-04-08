from setuptools import setup, find_packages

setup(
    name="devnotes",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
        "typer",
        "PyYAML",
        "python-dateutil",
        "prompt-toolkit",
    ],
    entry_points={
        "console_scripts": [
            "devnotes=devnotes.cli:app_cli",
        ],
    },
    author="Fabio",
    author_email="your.email@example.com",
    description="Un tool per gestire note di sviluppo e task di progetto",
    keywords="development, notes, tasks, project management",
    python_requires=">=3.7",
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "flake8",
            "black",
        ],
    },
)