# CloudFormation Template for Web and App Instances

## Overview

This CloudFormation template provisions two web instances and three app instances within a specified VPC. It also sets up a private Elastic Load Balancer (ELB) for the web instances, allowing for TCP traffic on ports 80 and 443. Each instance is tagged with a `Schedule` tag, and instances are named based on configurable patterns.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Parameters](#parameters)
- [Resources](#resources)
- [Outputs](#outputs)
- [Notes](#notes)

## Prerequisites

- An existing VPC
- At least two private subnets in the VPC
- Security groups for the web and app tiers
- An SSH key pair for accessing the instances
- A valid AMI ID for the desired instance type

## Usage

To use this template, follow these steps:

1. Navigate to the AWS CloudFormation console.
2. Create a new stack.
3. Upload this template file or provide the S3 URL where the template is stored.
4. Fill in the required parameters.
5. Review and create the stack.

## Parameters

| Parameter              | Type                         | Description                                             | Default       |
|-----------------------|------------------------------|---------------------------------------------------------|---------------|
| `VpcId`               | AWS::EC2::VPC::Id           | VPC where the EC2 instances will be launched           | N/A           |
| `WebPrivateSubnetIds` | List<AWS::EC2::Subnet::Id   | Private Subnet IDs for the web tier instances          | N/A           |
| `AppPrivateSubnetIds` | List<AWS::EC2::Subnet::Id    | Private Subnet IDs for the app tier instances          | N/A           |
| `WebSecurityGroupId`  | AWS::EC2::SecurityGroup::Id  | Security Group ID for the web tier instances           | N/A           |
| `AppSecurityGroupId`  | AWS::EC2::SecurityGroup::Id  | Security Group ID for the app tier instances           | N/A           |
| `SSHKeyName`          | AWS::EC2::KeyPair::KeyName  | Name of the SSH key pair for EC2 instances             | N/A           |
| `WebInstanceType`     | String                       | EC2 instance type for web tier                          | t2.micro      |
| `AppInstanceType`     | String                       | EC2 instance type for app tier                          | t2.micro      |
| `AmiId`               | AWS::EC2::Image::Id         | AMI ID for the EC2 instances                            | N/A           |
| `DeviceName`          | String                       | EBS device name (e.g., /dev/sda1)                      | /dev/sda1     |
| `WebVolumeSize`       | Number                       | Volume size for web EC2 instances (in GB)              | 8             |
| `AppVolumeSize`       | Number                       | Volume size for app EC2 instances (in GB)              | 8             |
| `WebNamePattern`      | String                       | Name pattern for web tier instances                     | web-server-   |
| `AppNamePattern`      | String                       | Name pattern for app tier instances                     | app-server-   |

## Resources

The template creates the following resources:

- **2 Web EC2 Instances**: Named according to the specified `WebNamePattern`.
- **3 App EC2 Instances**: Named according to the specified `AppNamePattern`.
- **1 Private Load Balancer**: Internal load balancer to route traffic to web instances.
- **Target Groups**: For health checks and routing traffic to the web instances.
- **Listeners**: For handling TCP traffic on ports 80 and 443.

## Outputs

Upon successful creation of the stack, the following outputs will be available:

- **Instance Details**: A CSV format containing instance names, IDs, and private IP addresses.
- **ELB DNS Name**: The DNS name of the created private load balancer.
