from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chunktopus",
    version="0.1.2",
    author="Unsiloed AI",
    author_email="info@unsiloed.com",
    description="A multithreaded OCR API for document processing and chunking with simple interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Unsiloed-opensource/ocr-api-multithreaded",
    packages=find_packages(include=["chunktopus", "chunktopus.*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "uvicorn",
        "fastapi",
        "python-multipart",
        "python-dotenv",
        "pdf2image",
        "Pillow",
        "PyPDF2",
        "python-docx",
        "python-pptx",
        "openai",
        "numpy",
        "opencv-python-headless",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "chunktopus=chunktopus.cli:main",
        ],
    },
) 