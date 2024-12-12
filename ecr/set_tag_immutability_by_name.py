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
                'switched': 'No'  # Placeholder for tag immutability change status
            }

            matching_repositories.append(repo_info)

    return matching_repositories

def set_tag_immutability(ecr_client, repository_name):
    try:
        ecr_client.put_image_tag_mutability(
            repositoryName=repository_name,
            imageTagMutability='IMMUTABLE'
        )
        print(f"Tag immutability set for repository: {repository_name}")
        return 'Yes'
    except Exception as e:
        print(f"Failed to set tag immutability for repository {repository_name}: {e}")
        return 'No'

def main(region, pattern, profile, dry_run):
    boto3.setup_default_session(region_name=region, profile_name=profile)
    ecr_client = boto3.client('ecr')

    try:
        repositories = get_repositories(pattern)

        if not repositories:
            print(f"No repositories matching pattern '{pattern}' found.")
        else:
            output_file = 'repositories.csv'
            with open(output_file, mode='w', newline='') as csv_file:
                fieldnames = ['repositoryName', 'repositoryArn', 'tagImmutability', 'switched']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                for repo in repositories:
                    if 'snapshot' not in repo['repositoryName'].lower():
                        if dry_run:
                            print(f"Dry-run: Tag immutability would be set for repository: {repo['repositoryName']}")
                            repo['switched'] = 'Dry-Run'
                        else:
                            repo['switched'] = set_tag_immutability(ecr_client, repo['repositoryName'])
                    writer.writerow(repo)

            print(f"Repository data written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python script.py <region> <repository_name_pattern> <aws_profile> <dry_run>")
    else:
        region = sys.argv[1]
        pattern = sys.argv[2]
        profile = sys.argv[3]
        dry_run = sys.argv[4].lower() == 'true'
        main(region, pattern, profile, dry_run)

