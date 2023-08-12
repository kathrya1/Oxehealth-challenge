#!/usr/bin/python3
import argparse
import os

import boto3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Uploads files to S3")
    parser.add_argument(
        "-d", "--dir", default="test-files", help="The directory to upload files from"
    )
    parser.add_argument(
        "-b", "--bucket", default="kathtestbucket", help="The bucket to upload files to"
    )
    return parser.parse_args()


def upload_and_delete_files(dir: str, bucket: str) -> None:
    """
    Uploads all files of the correct format (.dat) to the bucket in s3, then deletes the file locally.
    """
    s3_client = boto3.client("s3")

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".dat"):
                print(f"Uploading {file}...")
                s3_client.upload_file(os.path.join(root, file), bucket, file)
                print(os.path.join(root, file))
                os.remove(os.path.join(root, file))
                print(f"Deleted {file}")


def clean_empty_dirs(dir):
    """
    Cleans up empty directories in the specified directory.
    """
    for root, dirs, files in os.walk(dir, topdown=False):
        for dir in dirs:
            full_path = os.path.join(root, dir)
            if not os.listdir(full_path):
                os.rmdir(full_path)


def main() -> None:
    """
    Uploads all files in the specified directory to S3.
    Then deletes the files.
    """
    args = parse_args()

    upload_and_delete_files(args.dir, args.bucket)

    clean_empty_dirs(args.dir)


if __name__ == "__main__":
    main()
