from setuptools import setup, find_packages

setup(
    name="fastapiFileManager",
    version="1.1.3",
    author="Joseph Christopher",
    author_email="joechristophersc@gmail.com",
    description="A simple file manager for FastAPI with optional cloud uploads",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emeraldlinks/fastapi_filemanager",
    packages=find_packages(),
    install_requires=[
        "fastapi"
    ],
    extras_require={
        "cloudinary": ["cloudinary"],
        "aws": ["boto3"],
        "firebase": ["firebase-admin"],
        "gcloud": ["google-cloud-storage"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.7",
)
