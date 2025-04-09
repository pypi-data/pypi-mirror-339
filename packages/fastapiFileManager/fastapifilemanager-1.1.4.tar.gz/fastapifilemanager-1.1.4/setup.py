from setuptools import setup, find_packages

setup(
    name="fastapiFileManager",
    version="1.1.4",
    author="Joseph Christopher",
    author_email="joechristophersc@gmail.com",
    description="A simple file manager for FastAPI with cloud support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emeraldlinks/fastapiFileManager",
    packages=find_packages(),
    install_requires=["fastapi", "aiofiles"],  
    extras_require={
        "cloudinary": ["cloudinary"],
        "aws": ["boto3"],
        "firebase": ["firebase-admin"],
        "gcloud": ["google-cloud-storage"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.7",
)
