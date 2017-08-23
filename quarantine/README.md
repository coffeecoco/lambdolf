# Auto MFA
An AWS Lambda function that reenables MFA if a user disables it. This will not work for the root user. _You cannot manage the MFA device for the root user with the AWS API, AWS CLI, Tools for Windows PowerShell, or any other command-line tool._

## Steps
1. Cloudtrail must be enabled and configured to send to Cloudwatch
1. Build IAM policy for Lambda role.
1. Create IAM Role with assigned policy you created.
1. Create Lambda Function with trigger as _CloudWatch Logs_, Create filter `MFA_Disabled` with pattern `{ ($.eventName=DeleteVirtualMFADevice) || ($.eventName=DeactivateMFADevice) }`, Attach Role you created
1. Build an Event Pattern that searches for _DeactivateMFADevice_, and _DeleteVirtualMFADevice_ eg `{ ($.eventName=DeleteVirtualMFADevice) || ($.eventName=DeactivateMFADevice) }`
1.

## Notes:
http://boto3.readthedocs.io/en/latest/reference/services/iam.html#IAM.VirtualMfaDevice
http://docs.aws.amazon.com/cli/latest/reference/iam/create-virtual-mfa-device.html
http://docs.aws.amazon.com/cli/latest/reference/iam/enable-mfa-device.html
