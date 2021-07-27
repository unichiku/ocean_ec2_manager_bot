import boto3

# YOUR OWN INSTANCE ID
instances = ['i-00000000000000000']


def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    ec2.stop_instances(InstanceIds=instances)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": "minecraft down down down ..."
        }
    }
