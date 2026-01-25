from setuptools import setup, find_packages

setup(
    name="linksanity",
    version="0.1.0",
    description="Organizador inteligente de bookmarks del navegador",
    author="LinkSanity Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "linksanity=linksanity.cli.interface:main",
        ],
    },
)
