import boto3

cfn = boto3.client('cloudformation')
ec2 = boto3.client('ec2')
try:
    print("Creating testcase3")
    response = cfn.create_stack(
        StackName='testcase3',
        TemplateURL='https://cfn-ap-southeast-5.s3.ap-southeast-5.amazonaws.com/test3/main.yaml',
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ],
        OnFailure='ROLLBACK',
        Parameters=[
            {
                'ParameterKey': 'VpcId',
                'ParameterValue': 'vpc-0c9ba9b68d530303f'
            }
        ]
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("create_stack" + response['ResponseMetadata'])
    waiter = cfn.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='testcase3'
    )
    print("Stack create complete")
    print("Get NestedStack")
    nested_stack = cfn.describe_stack_resource(
        StackName='testcase3',
        LogicalResourceId='NestedStackA'
    )
    print("NestedStackA arn - " +
          nested_stack['StackResourceDetail']['PhysicalResourceId'])
    sg_id_1 = cfn.describe_stack_resource(
        StackName=nested_stack['StackResourceDetail']['PhysicalResourceId'],
        LogicalResourceId='SecurityGroup1'
    )
    print(sg_id_1['StackResourceDetail']['PhysicalResourceId'])
    response = ec2.delete_security_group(
        GroupId=sg_id_1['StackResourceDetail']['PhysicalResourceId'],
    )
    print("SG deleted")
    print("Updating testcase3 stack")
    response = cfn.update_stack(
        StackName='testcase3',
        TemplateURL='https://cfn-ap-southeast-5.s3.ap-southeast-5.amazonaws.com/test3/updated_main.yaml',
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ],
        Parameters=[
            {
                'ParameterKey': 'VpcId',
                'ParameterValue': 'vpc-0c9ba9b68d530303f'
            }
        ]
    )
except Exception as err:
    print(err)
else:
    print("Nothing went wrong")
