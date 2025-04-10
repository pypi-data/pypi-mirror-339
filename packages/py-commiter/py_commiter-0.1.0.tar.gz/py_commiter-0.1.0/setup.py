from setuptools import setup, find_packages

setup(
    name="py-commiter",
    version="0.1.0",
    author="Matias Tillerias",
    description="A CLI tool to create Conventional Commits with emoji and scope selection.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MatiasTilleriasLey/py-commiter",  # Opcional
    packages=find_packages(),
    install_requires=[
        "prompt_toolkit",
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "py-commiter=py_commiter.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

