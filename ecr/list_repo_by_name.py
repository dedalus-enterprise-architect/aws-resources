import boto3
import csv
import re

def get_repositories(pattern):
    ecr_client = boto3.client('ecr')

    repositories = []
    paginator = ecr_client.get_paginator('describe_repositories')
    for page in paginator.paginate():
        repositories.extend(page['repositories'])

    matching_repositories = []
    for repo in repositories:
        if re.search(pattern, repo['repositoryName']):
            repo_info = {
                'repositoryName': repo['repositoryName'],
                'repositoryArn': repo['repositoryArn'],
                'tagImmutability': repo['imageTagMutability'],
                'imageCount': 0  # Placeholder, will be updated below
            }

            # Get image count
            image_paginator = ecr_client.get_paginator('list_images')
            image_count = 0
            for image_page in image_paginator.paginate(repositoryName=repo['repositoryName']):
                image_count += len(image_page['imageIds'])
            repo_info['imageCount'] = image_count

            matching_repositories.append(repo_info)

    return matching_repositories

def main(region, pattern, profile):
    boto3.setup_default_session(region_name=region, profile_name=profile)

    try:
        repositories = get_repositories(pattern)

        if not repositories:
            print(f"No repositories matching pattern '{pattern}' found.")
        else:
            output_file = 'repositories.csv'
            with open(output_file, mode='w', newline='') as csv_file:
                fieldnames = ['repositoryName', 'repositoryArn', 'tagImmutability', 'imageCount']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                for repo in repositories:
                    writer.writerow(repo)

            print(f"Repository data written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script.py <region> <repository_name_pattern> <aws_profile>")
    else:
        region = sys.argv[1]
        pattern = sys.argv[2]
        profile = sys.argv[3]
        main(region, pattern, profile)

