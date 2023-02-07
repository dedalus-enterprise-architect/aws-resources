import configparser
import boto3
import botocore
import eks_token
import os

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
    assumed_creds = eks_token.assume_role(role_arn)

    # Save assumed credentials to the local AWS CLI credentials and config files
    eks_token.write_aws_credentials(assumed_creds, profile_name='eks_assumed')
    eks_token.write_aws_config(region=session.region_name, profile_name='eks_assumed')

    # Update the EKS kubeconfig file
    eks_token.update_kubeconfig(cluster_name=cluster_name, profile_name='eks_assumed')
    print(f"EKS kubeconfig file updated for cluster '{cluster_name}'")

# Example usage
update_eks_kubeconfig(role_arn, cluster_name, profile_name)
