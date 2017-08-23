import boto3

session = boto3.Session(
    profile_name='evolveacademy',
    region_name='us-west2'
)

cloudwatch = boto3.client('cloudwatch')

iam = boto3.resource('iam')


response = cloudwatch.list_metrics(
    Namespace='LogMetrics'
)

print(response)
