import boto3

# using local creds for testing
session = boto3.Session(
    profile_name='evolveacademy',
    region_name='us-west2'
)


iam = boto3.client('iam')


# TODO Get IAM user and create a virtual device for them

response = iam.create_virtual_mfa_device(
    Path='/',
    VirtualMFADeviceName='jholcomb@evolvesecurity.ioMFADevice'
)


# TODO Parse out key params so we use in able
serial_number = response['VirtualMFADevice']['SerialNumber']

# For Debug
print(response)
print("\n\n")


# TODO Add Enabled MFA boto call
response = client.enable_mfa_device(
    UserName = 'string', # fix
    SerialNumber = serial_number,
    AuthenticationCode1 = 'string', # fix
    AuthenticationCode2 = 'string' # fix
)



# Delete IAM so we can keep running the script
iam.delete_virtual_mfa_device(
    SerialNumber = serial_number
)

# print responses to console

print(response)
print("\n\n")
