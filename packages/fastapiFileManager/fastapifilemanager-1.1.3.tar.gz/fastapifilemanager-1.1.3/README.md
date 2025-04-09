Project description
File Manager for FastAPI
A plug-and-play solution for managing file uploads in FastAPI apps. It handles file uploads, saves them uniquely, and serves them via a static route automatically. It also supports cloud storage solutions like Cloudinary, AWS S3, Firebase, and Google Cloud Storage.
GitHub Repository

Installation
Install using pip:

bash
Copy
Edit
pip install fastapiFileManager
Quick Start
fastapiFileManager is designed to be a plug-and-play package to manage files in FastAPI, just like in Django. You only need three lines of code to get started:

python
Copy
Edit
from fastapiFileManager import FileManager
file_manager = FileManager(app=app, base_path="uploads", route_path="/files")

file_url = file_manager.save_file(file)
Full Example:
python
Copy
Edit
from fastapi import FastAPI, UploadFile
from fastapiFileManager import FileManager

app = FastAPI()

# Initialize FileManager (can be configured to use Cloud services)
file_manager = FileManager(
    app=app,
    cloud="cloudinary",  # Options: 'local', 'cloudinary', 'aws', 'firebase', 'gcloud'
    base_path="uploads",  # Only used for local storage
    route_path="/files",
    cloud_config={
        "cloud_name": "your_cloudinary_name",
        "api_key": "your_api_key",
        "api_secret": "your_api_secret",
        # Additional cloud config options for AWS, Firebase, GCloud, etc.
    }
)

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Save the file and get its URL
    file_url = file_manager.save_file(file)
    return {"file_url": file_url, "check as": f"localhost:8000/{file_url}"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    # Serve the file for download
    return file_manager.serve_file(filename)
Features:
Plug-and-play solution: Just integrate and start managing files.

Automatic file serving: Files are served via a static route (for local storage).

Cloud storage support: Supports file uploads to Cloudinary, AWS S3, Firebase, and Google Cloud Storage.

Simple API: Easy to use methods to upload, save, and serve files.

Customizable paths: Specify the base path for saving and the route for serving files.

Cloud Storage Support
Cloudinary: A popular cloud service for media management.

AWS S3: Upload files directly to AWS S3 buckets.

Firebase: Upload files to Firebase Storage and make them publicly accessible.

Google Cloud Storage: Upload files to Google Cloud Storage and manage them with public URLs.

Configuration
Cloud Option: In the FileManager constructor, you can choose your cloud provider with the cloud argument. The options are:

'local': Use the local filesystem (default).

'cloudinary': Use Cloudinary for storing files.

'aws': Use Amazon S3 for storing files.

'firebase': Use Firebase Storage for storing files.

'gcloud': Use Google Cloud Storage for storing files.

Cloud Config: You can pass a dictionary containing the necessary configuration for your cloud provider in the cloud_config argument:

For Cloudinary, provide cloud_name, api_key, and api_secret.

For AWS S3, provide aws_access_key_id, aws_secret_access_key, and bucket.

For Firebase, provide the firebase_credentials path and firebase_bucket.

For Google Cloud Storage, provide gcloud_credentials and bucket.

