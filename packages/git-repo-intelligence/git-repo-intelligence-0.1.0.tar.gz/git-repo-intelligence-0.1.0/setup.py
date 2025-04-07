from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-repo-intelligence",
    version="0.1.0",
    author="Mehul Prajapati",
    author_email="mehulprajapati2802@gmail.com",
    description="Git Repository Intelligence Platform - AI-driven repository insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehulprajapati2802/git-repo-intelligence",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
    install_requires=[
        "gitpython>=3.1.30",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "nltk>=3.8.0",
        "requests>=2.28.0",
        "openai>=0.27.0",
    ],
    extras_require={
        "pdf": ["pdfkit>=1.0.0"],
        "markdown": ["markdown>=3.4.0"],
        "full": [
            "pdfkit>=1.0.0",
            "markdown>=3.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "git-intelligence=git_repo_intelligence:main",
        ],
    },
    keywords="git, analytics, repository, insights, ai, llm, developer, intelligence",
    include_package_data=True,
) 