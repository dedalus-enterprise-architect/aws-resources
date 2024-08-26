#!/bin/bash

# Check if the required parameters are provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <repositories_file> <aws_region> <aws_profile>"
  exit 1
fi

# Parameters
REPOSITORIES_FILE="$1"
AWS_REGION="$2"
AWS_PROFILE="$3"


# Read the file line by line
while IFS= read -r repo_name; do
  if [ -n "$repo_name" ]; then
    # Create the repository
    echo "Creating repository: $repo_name"
    aws ecr create-repository --repository-name "$repo_name" --region $AWS_REGION --profile $AWS_PROFILE

    # Check if the repository name does not contain "snapshot"
    if [[ "$repo_name" != *"snapshot"* ]]; then
      echo "Setting image immutability for repository: $repo_name"
      aws ecr put-image-tag-mutability --repository-name "$repo_name" --image-tag-mutability IMMUTABLE --region $AWS_REGION --profile $AWS_PROFILE
    fi
  fi
done < "$REPOSITORIES_FILE"

echo "All repositories have been processed."
