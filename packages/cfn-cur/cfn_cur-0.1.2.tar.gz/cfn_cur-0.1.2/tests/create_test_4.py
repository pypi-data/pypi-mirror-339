import boto3
import random

cfn = boto3.client('cloudformation')
ec2 = boto3.client('ec2')
try:
    print("Creating testcase4")
    response = cfn.create_stack(
        StackName='testcase4',
        TemplateURL='https://gosolo2.s3.amazonaws.com/testcase4/main.yml',
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ],
        Tags=[
            {
                'Key': 'testcase',
                'Value': '4'
            },
        ],
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("create_stack" + response['ResponseMetadata'])
    waiter = cfn.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='testcase4'
    )
    print("Stack create complete")
    print("Creating chaos")
    response = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'tag:testcase',
                'Values': [
                    '4',
                ]
            },
        ]
    )

    sg_s = [x['GroupId'] for x in response['SecurityGroups']]

    n_to_destroy = random.randint(1, len(sg_s))

    print(str(n_to_destroy)+" SG's will be deleted")

    while n_to_destroy > 0:
        ind_to_destroy = random.randint(0, len(sg_s)-1)
        to_delete = sg_s.pop(ind_to_destroy)
        response = ec2.delete_security_group(
            GroupId=to_delete,
        )
        n_to_destroy -= 1
    print("Chaos Complete")
    print("Updating testcase4 stack")
    response = cfn.update_stack(
        StackName='testcase4',
        TemplateURL='https://gosolo2.s3.amazonaws.com/testcase4/updated_main.yml',
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ]
    )
except Exception as err:
    print(err)
else:
    print("Nothing went wrong")
