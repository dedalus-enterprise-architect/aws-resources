# CloudFormation Template for VPC with 8 Subnets in 2 AZs

## Overview

This CloudFormation template provisions a VPC with 2 public subnets and 6 private subnets across 2 Availability Zones (AZs). It also includes optional Internet Gateway and NAT Gateway resources.

## Prerequisites

- AWS account with necessary permissions to create VPC, subnets, and other resources.
- AWS CLI or AWS Management Console access.

## Usage

To use this template, follow these steps:

1. Navigate to the AWS CloudFormation console.
2. Create a new stack.
3. Upload this template file or provide the S3 URL where the template is stored.
4. Fill in the required parameters.
5. Review and create the stack.

## Parameters

| Parameter              | Type    | Description                                      | Default       |
|------------------------|---------|--------------------------------------------------|---------------|
| `VpcName`              | String  | Name of the VPC                                  | N/A           |
| `VpcCidr`              | String  | CIDR block for the VPC                           | 172.20.0.0/16 |
| `CreateInternetGateway`| String  | Whether to create an Internet Gateway (true/false)| true          |
| `CreateNatGateway`     | String  | Whether to create a NAT Gateway (true/false)     | true          |
| `PublicSubnet1Cidr`    | String  | CIDR block for Public Subnet 1 in AZ-A           | 172.20.0.0/24 |
| `PublicSubnet2Cidr`    | String  | CIDR block for Public Subnet 2 in AZ-B           | 172.20.1.0/24 |
| `PrivateSubnet1Cidr`   | String  | CIDR block for Private Subnet 1 in AZ-A          | 172.20.2.0/24 |
| `PrivateSubnet2Cidr`   | String  | CIDR block for Private Subnet 2 in AZ-A          | 172.20.3.0/24 |
| `PrivateSubnet3Cidr`   | String  | CIDR block for Private Subnet 3 in AZ-A          | 172.20.4.0/24 |
| `PrivateSubnet4Cidr`   | String  | CIDR block for Private Subnet 4 in AZ-B          | 172.20.5.0/24 |
| `PrivateSubnet5Cidr`   | String  | CIDR block for Private Subnet 5 in AZ-B          | 172.20.6.0/24 |
| `PrivateSubnet6Cidr`   | String  | CIDR block for Private Subnet 6 in AZ-B          | 172.20.7.0/24 |

## Resources

The template creates the following resources:

- **VPC**: A Virtual Private Cloud with the specified CIDR block.
- **Public Subnets**: 2 public subnets, one in each AZ.
- **Private Subnets**: 6 private subnets, three in each AZ.
- **Internet Gateway**: An optional Internet Gateway for the VPC.
- **NAT Gateway**: An optional NAT Gateway for the VPC.
- **Route Tables**: Route tables for public and private subnets.
- **Route Table Associations**: Associations between subnets and route tables.

## Outputs

Upon successful creation of the stack, the following outputs will be available:

- **VpcId**: The ID of the created VPC.
- **PublicSubnet1Id**: The ID of Public Subnet 1.
- **PublicSubnet2Id**: The ID of Public Subnet 2.
- **PrivateSubnet1Id**: The ID of Private Subnet 1.
- **PrivateSubnet2Id**: The ID of Private Subnet 2.
- **PrivateSubnet3Id**: The ID of Private Subnet 3.
- **PrivateSubnet4Id**: The ID of Private Subnet 4.
- **PrivateSubnet5Id**: The ID of Private Subnet 5.
- **PrivateSubnet6Id**: The ID of Private Subnet 6.
