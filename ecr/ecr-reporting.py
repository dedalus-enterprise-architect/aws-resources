import json
import boto3
import csv
from datetime import datetime

def lambda_handler(event, context):
    # Connect to ECR
    ecr_client = boto3.client("ecr")

    # List all repositories in ECR
    response = ecr_client.describe_repositories()
    repositories = response['repositories']

    # Initialize the data structure to store the image information
    data = []

    # Loop through each repository
    for repository in repositories:
        repository_name = repository['repositoryName']

        # List all image tags for the repository
        response = ecr_client.list_images(repositoryName=repository_name)
        image_details = response['imageIds']

        # Loop through each image in the repository
        for image_detail in image_details:
            # Retrieve the image tag, digest, and size
            image_tag = image_detail.get('imageTag', '')
            image_digest = image_detail['imageDigest']
            response = ecr_client.describe_images(repositoryName=repository_name, imageIds=[{'imageDigest': image_digest}])
            image_size = response['imageDetails'][0]['imageSizeInBytes']

            # Store the image information
            data.append({
                'repository_name': repository_name,
                'image_tag': image_tag,
                'image_digest': image_digest,
                'image_size': image_size
            })

    # Dump the data to a JSON file in S3
    s3_client = boto3.client("s3")
    bucket_name = "my-s3-bucket"
    date = datetime.now().strftime("%Y-%m-%d")
    json_file_name = f"ecr_images_{date}.json"
    s3_client.put_object(Bucket=bucket_name, Key=json_file_name, Body=json.dumps(data))

    # Dump the data to a CSV file in S3
    csv_file_name = f"ecr_images_{date}.csv"
    with open(csv_file_name, "w") as f:
        writer = csv.DictWriter(f, fieldnames=['repository_name', 'image_tag', 'image_digest', 'image_size'], delimiter="|")
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    with open(csv_file_name, "rb") as f:
        s3_client.put_object(Bucket=bucket_name, Key=csv_file_name, Body=f.read())

    return "Data dumped to S3 successfully"
