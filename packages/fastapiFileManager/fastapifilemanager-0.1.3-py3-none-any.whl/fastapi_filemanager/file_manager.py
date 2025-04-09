from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil

# Cloud support imports
import cloudinary
from cloudinary import uploader as cloudinary_uploader
import boto3
from google.cloud import storage as gcs_storage
import firebase_admin
from firebase_admin import credentials, storage as firebase_storage

__version__ = "0.1.3"


class FileManager:
    def __init__(self, app: FastAPI, cloud: str = 'local', base_path: str = "uploads", cloud_config: dict = {}):
        self.cloud = cloud
        self.base_path = base_path
        self.cloud_config = cloud_config

        if self.cloud == "local":
            os.makedirs(self.base_path, exist_ok=True)
            app.mount("/static", StaticFiles(directory=self.base_path), name="static")

        elif self.cloud == "cloudinary":
            cloudinary.config(
                cloud_name=self.cloud_config["cloud_name"],
                api_key=self.cloud_config["api_key"],
                api_secret=self.cloud_config["api_secret"]
            )

        elif self.cloud == "firebase" and not firebase_admin._apps:
            cred_path = self.cloud_config.get("firebase_credentials")
            if not cred_path:
                raise Exception("Firebase credentials file path required in cloud_config['firebase_credentials']")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'storageBucket': self.cloud_config.get("firebase_bucket")
            })

    def save_file(self, file: UploadFile) -> str:
        try:
            file_ext = os.path.splitext(file.filename)[-1]
            unique_name = f"{uuid.uuid4().hex}{file_ext}"

            if self.cloud == "cloudinary":
                res = cloudinary_uploader.upload(file.file, public_id=unique_name)
                return res["secure_url"]

            elif self.cloud == "aws":
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=self.cloud_config["aws_access_key_id"],
                    aws_secret_access_key=self.cloud_config["aws_secret_access_key"]
                )
                s3.upload_fileobj(file.file, self.cloud_config["bucket"], unique_name)
                return f"https://{self.cloud_config['bucket']}.s3.amazonaws.com/{unique_name}"

            elif self.cloud == "firebase":
                bucket = firebase_storage.bucket()
                blob = bucket.blob(unique_name)
                blob.upload_from_file(file.file)
                blob.make_public()
                return blob.public_url

            elif self.cloud == "gcloud":
                client = gcs_storage.Client.from_service_account_json(self.cloud_config["gcloud_credentials"])
                bucket = client.bucket(self.cloud_config["bucket"])
                blob = bucket.blob(unique_name)
                blob.upload_from_file(file.file)
                blob.make_public()
                return blob.public_url

            else:  # local
                file_path = os.path.join(self.base_path, unique_name)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                return f"/static/{unique_name}"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
