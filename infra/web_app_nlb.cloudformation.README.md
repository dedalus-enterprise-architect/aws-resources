# AWS CloudFormation Template for EC2 Instances in Auto Scaling Groups with NLBs

This CloudFormation template provisions EC2 instances for **Web** and **App** tiers in separate Auto Scaling Groups (ASGs), with optional **Network Load Balancers (NLBs)** for each tier. You can customize the instance types, number of instances, AMI, security groups, and the block device mappings including EBS volume sizes. The NLBs are internal by default and are only created if specified.

## Table of Contents

- [Parameters](#parameters)
- [Resources Created](#resources-created)
- [NLB Provisioning](#nlb-provisioning)
- [Tags](#tags)
- [Usage](#usage)
- [Example Stack Creation](#example-stack-creation)

## Parameters

### Required Parameters

| Parameter               | Description                                         |
|-------------------------|-----------------------------------------------------|
| **VpcId**                | VPC where the EC2 instances will be launched.       |
| **WebSubnetIds**         | List of subnet IDs for the web tier instances.      |
| **AppSubnetIds**         | List of subnet IDs for the app tier instances.      |
| **WebSecurityGroupId**   | Security Group ID for the web tier instances.       |
| **AppSecurityGroupId**   | Security Group ID for the app tier instances.       |
| **SSHKeyName**           | Name of the SSH key pair for EC2 instances.         |
| **AmiId**                | AMI ID for the EC2 instances.                      |

### Optional Parameters

| Parameter               | Default         | Description                                                                                               |
|-------------------------|-----------------|-----------------------------------------------------------------------------------------------------------|
| **WebInstanceCount**     | `1`             | Desired number of EC2 instances for the web tier.                                                          |
| **AppInstanceCount**     | `1`             | Desired number of EC2 instances for the app tier.                                                          |
| **WebInstanceType**      | `t2.micro`      | EC2 instance type for the web tier.                                                                        |
| **AppInstanceType**      | `t2.micro`      | EC2 instance type for the app tier.                                                                        |
| **WebNamePattern**       | `web-server-`   | Name pattern for the web tier instances.                                                                   |
| **AppNamePattern**       | `app-server-`   | Name pattern for the app tier instances.                                                                   |
| **DeviceName**           | `/dev/sda1`     | EBS device name. <br>**Tip**: For Amazon Linux, set to `/dev/xvda`. For Oracle Linux, set to `/dev/sda1`.  |
| **VolumeSize**           | `8`             | The size of the EBS volume in GiB.                                                                         |
| **ProvisionWebNLB**      | `false`         | Whether to provision an internal NLB for the web tier (`true`/`false`).                                    |
| **ProvisionAppNLB**      | `false`         | Whether to provision an internal NLB for the app tier (`true`/`false`).                                    |
| **WebNLBTCPPort**        | `80`            | TCP port for the Web NLB listener.                                                                         |
| **AppNLBTCPPort**        | `8080`          | TCP port for the App NLB listener.                                                                         |

## Resources Created

The template creates the following resources:

| Resource                    | Description                                                                                                                                                       |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Launch Templates**         | Launch templates for both Web and App tiers, with custom instance types, AMI, EBS volumes, and security groups.                                                   |
| **Auto Scaling Groups (ASGs)**| Auto Scaling Groups (ASGs) for scaling EC2 instances based on demand, with desired instance counts and capacity specified by the user.                            |
| **NLBs (optional)**          | Internal Network Load Balancers for the Web and App tiers, created in the specified private subnets, with TCP listeners and target groups for traffic routing.    |
| **EBS Volumes**              | Attached to the EC2 instances with the size and device name specified by the user.                                                                                 |

## NLB Provisioning

- NLBs are **optional** and can be enabled or disabled via the parameters `ProvisionWebNLB` and `ProvisionAppNLB`.
- When enabled, the NLBs are created with the **internal** scheme (not publicly accessible).
- Health checks for the NLBs are done over **TCP** on the specified ports for both Web and App tiers.

## Tags

All provisioned resources (EC2 instances, NLBs, etc.) are tagged with the CloudFormation stack name for easy identification and management.  
Each resource will have the following tag:

| Tag Key     | Tag Value                    |
|-------------|------------------------------|
| **Name**    | `<stack-name>`                |

## Usage

### Pre-Requisites

| Pre-Requisite                | Description                                                                                   |
|------------------------------|-----------------------------------------------------------------------------------------------|
| **VPC**                      | An existing VPC in which to deploy the EC2 instances and optional NLBs.                       |
| **Security Groups**           | Pre-existing security groups for the Web and App tiers.                                       |
| **Private Subnets**           | Subnet IDs must belong to **private** subnets for provisioning the internal NLBs.             |

### How to Use

1. **Download the CloudFormation Template**: Save the CloudFormation YAML file to your local machine.
2. **Launch the CloudFormation Stack**:
   - Open the AWS Management Console.
   - Navigate to **CloudFormation**.
   - Click **Create Stack** and upload the YAML file.
3. **Fill in the Parameters**: During stack creation, provide the required parameters like `VpcId`, `WebSubnetIds`, `AppSubnetIds`, and `AmiId`.
4. **Monitor Stack Creation**: The resources will be provisioned as per the specified configurations.
5. **Access NLB**: If NLBs are enabled, you can retrieve their DNS names from the stack outputs after successful provisioning.

## Example Stack Creation

Here’s an example of how to create the stack using the AWS CLI:

```bash
aws cloudformation create-stack \
    --stack-name my-ec2-asg-stack \
    --template-body file://ec2-asg-nlb-template.yaml \
    --parameters ParameterKey=VpcId,ParameterValue=vpc-01234567 \
                 ParameterKey=WebSubnetIds,ParameterValue="subnet-abc12345,subnet-def67890" \
                 ParameterKey=AppSubnetIds,ParameterValue="subnet-ghi12345,subnet-jkl67890" \
                 ParameterKey=AmiId,ParameterValue=ami-0abcdef1234567890
