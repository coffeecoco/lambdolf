# Quarantine Users
This Lambda function will quarantine an IAM user by disabling
1. Console login
1. Programmatic access (access keys)
1. Group memberships
1. Directly attached policies

This repository provides details on the following suggested triggers for the lambda function.
1. MFA Device is deactivated or deleted.

## IAM Policy
In addition to the AWSLambdaBasicExecutionRole IAM policy, this is the required IAM policy that must be attached to the Lambda Role: [iam-policy.json](iam-policy.json)

### Use Case: Trigger on "MFA Device is Deactivated"

#### Description
Quarantine a user if MFA is disabled on their IAM account. Please test a dummy user account before enabling the trigger.

#### Setup
1. Create the IAM policy above for the Lambda Role.
1. Create IAM Role and assign the above IAM policy.
1. Create a new Lambda function:
  * Choose _Author from scratch_
  * Skip the _Configure triggers section_
  * Select _Python 3.6_ for the runtime
  * Paste source code from [quarantine.py](quarantine.py)
  * Select _Choose an existing role_ and apply the Role you created
1. Create a new rule in CloudWatch with the Event Pattern:

  ```
  {
    "source": [
      "aws.iam"
    ],
    "detail": {
      "eventName": [
        "DeactivateMFADevice",
        "DeleteVirtualMFADevice"
      ]
    }
  }
  ```
  * Select _Add a target_ and add your Lambda function
