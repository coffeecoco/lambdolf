import boto3

class Error(Exception):
    def __init__(self, message):
        self.message = message

def get_event_user_name(event):
    if not "detail" in event:
        raise Error("No 'detail' in event.")
    elif not "requestParameters" in event["detail"]:
        raise Error("No 'requestParameters' in event['detail'].")
    elif not "requestParameters" in event["detail"]:
        raise Error("No 'requestParameters' in event['detail'].")
    elif not "userName" in event["detail"]["requestParameters"]:
        raise Error("No 'userName' in event['detail']['requestParameters'].")
    return event["detail"]["requestParameters"]["userName"]

def remove_access_keys(iam, user_name):
    print('removing access keys...')
    access_keys_response = iam.list_access_keys(
        UserName = user_name,
        MaxItems=100
    )
    if not "AccessKeyMetadata" in access_keys_response:
        raise Error("No 'AccessKeyMetadata' in user_access_keys_response")
    access_keys = access_keys_response["AccessKeyMetadata"]
    removed_access_key_ids = []
    for access_key in access_keys:
        if not "AccessKeyId" in access_key:
            continue
        access_key_id = access_key["AccessKeyId"]
        response = iam.delete_access_key(
            UserName = user_name,
            AccessKeyId = access_key_id
        )
        removed_access_key_ids.append(access_key_id)

    return removed_access_key_ids

def get_attached_policies(iam, user_name):
    response = iam.list_attached_user_policies(
        UserName=user_name
    )
    return response["AttachedPolicies"]

def get_user_policy_names(iam, user_name):
    response = iam.list_user_policies(
        UserName=user_name
    )
    return response["PolicyNames"]

def detach_policy(iam, user_name, policy_arn):
    iam.detach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    return True

def delete_user_policy(iam, user_name, policy_name):
    iam.delete_user_policy(
        UserName=user_name,
        PolicyName=policy_name
    )
    return True

def remove_policies(iam, user_name):
    print('removing attached policies...')
    attached_policies = get_attached_policies(iam, user_name)
    removed_policies = []
    for policy in attached_policies:
        policy_name = policy["PolicyName"]
        policy_arn = policy["PolicyArn"]
        is_removed = detach_policy(iam, user_name, policy_arn)
        if is_removed:
            removed_policies.append(policy_name)

    print('removing user policies...')
    user_policy_names = get_user_policy_names(iam, user_name)
    for policy_name in user_policy_names:
        is_deleted = delete_user_policy(iam, user_name, policy_name)
        if is_deleted:
            removed_policies.append(policy_name)
    return removed_policies

def remove_groups(iam, user_name):
    print('removing groups...')
    response = iam.list_groups_for_user(
        UserName=user_name,
        MaxItems=100
    )
    groups = response["Groups"]
    removed_groups = []
    for group in groups:
        group_name = group["GroupName"]
        iam.remove_user_from_group(
            UserName=user_name,
            GroupName=group_name
        )
        removed_groups.append(group_name)
    return removed_groups

def delete_login_profile(iam, user_name):
    response = iam.delete_login_profile(
        UserName = user_name
    )
    is_deleted = False
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        is_deleted = True
    return is_deleted


def summary(user_name, key_ids, policies, groups, is_profile_deleted):
    message = ""
    message = "{}User: {}".format(message, user_name)
    message = "{}\n\nRemoved Access Keys Ids:".format(message)
    for key_id in key_ids:
        message = "{}\nKey Id: {}".format(message, key_id)
    message = "{}\n\nRemoved Policy Names:".format(message)
    for policy_name in policies:
        message = "{}\nPolicy Name: {}".format(message, policy_name)
    message = "{}\n\nRemoved Group Names:".format(message)
    for group_name in groups:
        message = "{}\nGroup Name: {}".format(message, group_name)
    message = "{}\n\nIs Profile Delete: {}".format(message, is_profile_deleted)
    print(message)
    return message

def handler(event, context):
    try:
        # check for the existence of detail, userIdentity, userName
        # using local creds for testing
        session = boto3.Session(
            profile_name='evolveacademy',
            region_name='us-west2'
        )
        iam = boto3.client('iam')

        user_name = get_event_user_name(event)

        key_ids = remove_access_keys(iam, user_name)

        policies = remove_policies(iam, user_name)

        groups = remove_groups(iam, user_name)

        is_profile_deleted = delete_login_profile(iam, user_name)

        return summary(user_name, key_ids, policies, groups, is_profile_deleted)

    except Error as err:
        print(err.message)
        return err.message
if __name__ == '__main__':
    lambda_handler({
        "detail":{
            "userIdentity":{
                "userName":"dead@evolveacademy.io",
                "accessKeyId": "AKIAJO2XAXDR4NSTQWQQ"
            }
        }
    }, {})
