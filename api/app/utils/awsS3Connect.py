import boto3
from botocore.exceptions import ClientError
from ..config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)


def upload_file_to_s3(file, filename: str):
    try:
        print("Bucket Name:", settings.AWS_S3_MAIN_CV_BUCKET_NAME)
        s3_client.upload_fileobj(
            file,
            settings.AWS_S3_MAIN_CV_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": "application/pdf"}
        )
        print("File uploaded successfully to S3")
        url = f"https://{settings.AWS_S3_MAIN_CV_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
        return url

    except ClientError as e:
        print("THIS IS THE ERROR: " , e)
        return None