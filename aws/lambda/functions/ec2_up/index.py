import boto3

# YOUR OWN INSTANCE ID
INSTANCE_ID = 'i-00000000000000000'
ALLOWED_INSTANCE_TYPES = ['t3a.large', 'm5n.large']


def lambda_handler(event, context):
    new_instance_type = event['instance_type']
    if not new_instance_type in ALLOWED_INSTANCE_TYPES:
        return response_maker(400, "[ERROR!] invalid instance_type")

    ec2 = boto3.client("ec2")

    # only running instance will return
    description = ec2.describe_instance_status(
        InstanceIds=[INSTANCE_ID],
        IncludeAllInstances=True
    )
    instance_state = description['InstanceStatuses'][0]['InstanceState']['Name']

    if instance_state != 'stopped':
        return response_maker(400, "[ERROR!] ec2 instance is not in 'stopped' state")

    ec2.modify_instance_attribute(
        InstanceId=INSTANCE_ID,
        Attribute='instanceType',
        Value=new_instance_type
    )
    ec2.start_instances(InstanceIds=[INSTANCE_ID])

    return response_maker(200, "minecraft up up up ...")


def response_maker(status, message):
    return {
        "isBase64Encoded": True,
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": {
            "message": message
        }
    }
