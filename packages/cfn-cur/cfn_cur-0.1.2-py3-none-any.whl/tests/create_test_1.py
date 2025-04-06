import boto3
import unittest
boto3.set_stream_logger('')
cfn = boto3.client('cloudformation')
ec2 = boto3.client('ec2')
try:
    print("Creating testcase1")
    bucket_name = 'cfn-ap-southeast-5'
    response = cfn.create_stack(
        StackName='testcase1',
        TemplateURL='https://cfn-ap-southeast-5.s3.ap-southeast-5.amazonaws.com/test1/stack.yaml',
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ],
        OnFailure='ROLLBACK',
        Parameters=[
            {
                'ParameterKey': 'VPCID',
                'ParameterValue': 'vpc-0c9ba9b68d530303f'
            }
        ]
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("create_stack" + response['ResponseMetadata'])
    waiter = cfn.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='testcase1'
    )
    print("Stack create complete")
    print("Get SG")
    sg_id = cfn.describe_stack_resource(
        StackName='testcase1',
        LogicalResourceId='InstanceSecurityGroup'
    )
    print("SG ID to delete - " +
          sg_id['StackResourceDetail']['PhysicalResourceId'])
    response = ec2.delete_security_group(
        GroupId=sg_id['StackResourceDetail']['PhysicalResourceId'],
    )
    print("SG deleted")
    print("Updating testcase1 stack")
    response = cfn.update_stack(
        StackName='testcase1',
        TemplateURL='https://cfn-ap-southeast-5.s3.ap-southeast-5.amazonaws.com/test1/updated_stack.yaml',
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ],
        Parameters=[
            {
                'ParameterKey': 'VPCID',
                'ParameterValue': 'vpc-0c9ba9b68d530303f'
            }
        ]
    )
except Exception as err:
    print(err)
else:
    print("Nothing went wrong")
