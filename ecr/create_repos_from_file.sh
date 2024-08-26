#!/bin/bash

# Check if the input file is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <repositories_file>"
  exit 1
fi

# Read the file line by line
while IFS= read -r repo_name; do
  if [ -n "$repo_name" ]; then
    # Create the repository
    echo "Creating repository: $repo_name"
    aws ecr create-repository --repository-name "$repo_name" --region "$AWS_REGION" --profile "$AWS_PROFILE"

    # Check if the repository name does not contain "snapshot"
    if [[ "$repo_name" != *"snapshot"* ]]; then
      echo "Setting image immutability for repository: $repo_name"
      aws ecr put-image-tag-mutability --repository-name "$repo_name" --image-tag-mutability IMMUTABLE --region "$AWS_REGION" --profile "$AWS_PROFILE"
    fi
  fi
done < "$1"

echo "All repositories have been processed."
