import configparser
import boto3
import botocore
import os
import subprocess

# Get the directory containing the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Load parameters from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, 'config.ini'))
profile_name = config.get("settings", "aws_session_profile")
role_arn = config.get("settings", "aws_role_arn")
cluster_name = config.get("settings", "eks_cluster_name")

def update_eks_kubeconfig(role_arn, cluster_name, profile_name):
    # Load AWS credentials and config files
    session = boto3.session.Session(profile_name=profile_name)
    creds = session.get_credentials()
    access_key = creds.access_key
    secret_key = creds.secret_key
    region = session.region_name

    # Assume the role
    sts_client = boto3.client('sts',
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,
                             region_name=region)
    assumed_role = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="UpdateEksKubeconfigSession")
    assumed_creds = assumed_role['Credentials']

    # Update the EKS kubeconfig file using the AWS CLI
    subprocess.run(["aws", "eks", "update-kubeconfig", "--name", cluster_name, "--role-arn", role_arn, "--access-key", assumed_creds['AccessKeyId'], "--secret-key", assumed_creds['SecretAccessKey'], "--session-token", assumed_creds['SessionToken']], check=True)
    print(f"EKS kubeconfig file updated for cluster '{cluster_name}'")

# Example usage
update_eks_kubeconfig(role_arn, cluster_name, profile_name)
