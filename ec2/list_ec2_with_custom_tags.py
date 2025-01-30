import boto3
import csv
import argparse

def get_ec2_instances(region, profile):
    session = boto3.Session(profile_name=profile)
    ec2_client = session.client('ec2', region_name=region)

    instances_data = []

    # Describe instances
    response = ec2_client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Extract instance details
            instance_id = instance.get('InstanceId', 'N/A')
            state = instance.get('State', {}).get('Name', 'N/A')
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            instance_type = instance.get('InstanceType', 'N/A')
            platform_details = instance.get('PlatformDetails', 'N/A')
            state_transition_reason = instance.get('StateTransitionReason', 'N/A')
            state_transition_message = instance.get('StateTransitionReason', 'N/A')  # Adding state transition message
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}

            # Retrieve tags and set defaults if missing
            instance_name = tags.get('Name', 'N/A')
            costo = tags.get('Costo', 'null')
            requested_by = tags.get('RequestedBy', 'null')
            referente = tags.get('Referente', 'null')
            owner = tags.get('Owner', 'null')

            instances_data.append({
                'Instance ID': instance_id,
                'Instance Name': instance_name,
                'Status': state,
                'Private IPv4 Address': private_ip,
                'Instance Type': instance_type,
                'Platform Details': platform_details,
                'State Transition Reason': state_transition_reason,
                'State Transition Message': state_transition_message,  # Adding state transition message to output
                'Costo': costo,
                'RequestedBy': requested_by,
                'Referente': referente,
                'Owner': owner
            })

    return instances_data

def write_to_csv(instances_data, output_file):
    fieldnames = [
        'Instance ID', 'Instance Name', 'Status', 'Private IPv4 Address',
        'Instance Type', 'Platform Details', 'State Transition Reason',
        'State Transition Message',  # Adding state transition message to CSV
        'Costo', 'RequestedBy', 'Referente', 'Owner'
    ]

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(instances_data)

    print(f"Data successfully written to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Retrieve EC2 instance details and export to CSV.")
    parser.add_argument('--region', required=True, help="AWS region, e.g., 'us-west-2'")
    parser.add_argument('--profile', required=True, help="AWS CLI profile name")
    parser.add_argument('--output', default='ec2_instances.csv', help="Output CSV file name")

    args = parser.parse_args()

    # Retrieve instances and write to CSV
    instances_data = get_ec2_instances(region=args.region, profile=args.profile)
    write_to_csv(instances_data, args.output)

if __name__ == '__main__':
    main()

