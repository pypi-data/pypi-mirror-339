from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="neuradoc",
    version="0.1.0",
    author="NeuraDoc Team",
    author_email="neuradoc@example.com",
    description="A Python package for parsing and transforming various document formats into LLM-ready data with element classification capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neuradoc/neuradoc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyPDF2>=2.0.0",
        "python-docx>=0.8.11",
        "openpyxl>=3.0.10",
        "beautifulsoup4>=4.10.0",
        "lxml>=4.6.5",
        "pillow>=9.0.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "python-pptx>=0.6.21",
        "requests>=2.27.0",
    ],
    extras_require={
        "ocr": ["pytesseract>=0.3.8"],
        "tables": ["camelot-py>=0.10.1", "tabula-py>=2.3.0"],
        "nlp": ["spacy>=3.2.0"],
        "transformers": ["transformers>=4.16.0", "torch>=1.10.0"],
        "web": ["flask>=2.0.0", "gunicorn>=20.0.0"],
    },
    project_urls={
        "Bug Tracker": "https://github.com/neuradoc/neuradoc/issues",
        "Documentation": "https://github.com/neuradoc/neuradoc",
        "Source Code": "https://github.com/neuradoc/neuradoc",
    },
    include_package_data=True,
    package_data={
        "neuradoc": ["**/*.py"],
    },
)
