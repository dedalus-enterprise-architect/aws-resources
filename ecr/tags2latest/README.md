# tag2latest_cloudformation.yaml

_WARNING: to test !_

## Overview

This CloudFormation template is designed to manage an EventBridge Rule, IAM role, and Lambda function to update the tags on ECR repositories.

## Author

- **Name:** Claudio Prato
- **Team:** Team EA
- **Create Date:** 2024/12/10

## Purpose

The primary purpose is to ensure that the latest image push matches the tag `latest`.

## CloudFormation Template Details

### Parameters

- **RepositoryNames**
  - **Type:** List<String>
  - **Description:** List of repository names to monitor with EventBridge.
  - **Default:**
    - `products/<organization_name>/<application_name1>`
    - `products/<organization_name>/<application_name2>`
    - `products/<organization_name>/<application_name3>`

### Resources

#### EventBridge Rule

- **Name:** anoki_push_latest_on_smarthospital
- **EventPattern:**
  - **Source:** `aws.ecr`
  - **Detail-Type:** `ECR Image Action`
  - **Detail:**
    - **Action-Type:** `PUSH`
    - **Result:** `SUCCESS`
    - **Repository-Name:** List of repository names from `RepositoryNames` parameter
- **State:** ENABLED
- **Description:** The last image push must match by the TAG: latest
- **EventBusName:** default
- **Targets:**
  - **Id:** LambdaTarget
  - **Arn:** Lambda function ARN

#### Lambda Function

- **FunctionName:** ecr_update_to_latest_onPush
- **Handler:** index.lambda_handler

## Special Notes

This repository aims to distribute a GitHub runner in a local environment.

## Usage

To deploy this CloudFormation template, use the AWS Management Console, AWS CLI, or any other tool that supports AWS CloudFormation.

```bash
aws cloudformation create-stack \
--stack-name my-stack \
--template-body file://tag2latest_cloudformation.yaml \
--parameters ParameterKey=RepositoryNames,ParameterValue=products/smart-hospital/cms-backoffice,products/smart-hospital/cms-webapp,products/smart-hospital/cms-server
```
