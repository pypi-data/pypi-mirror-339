import unittest
import boto3
import subprocess
from helpers.Helpers import Helpers


class TestCase1(unittest.TestCase):

    def setUp(self):
        self.cfn = boto3.client('cloudformation')
        self.ec2 = boto3.client('ec2')
        self.helpers = Helpers()
        self.helpers.upload_to_s3('stack.yml', 'muralikl', '1')
        self.helpers.upload_to_s3('updated_stack.yml', 'muralikl', '1')

    def test_case_1(self):
        stack_name = 'testcase1'
        try:
            print("Creating testcase1")
            response = self.cfn.create_stack(
                StackName=stack_name,
                TemplateURL='https://muralikl.s3.amazonaws.com/testcase1/stack.yml',
                OnFailure='ROLLBACK'
            )
            stack_arn = response['StackId']
            print(stack_arn)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception("create_stack" + response['ResponseMetadata'])
            waiter = self.cfn.get_waiter('stack_create_complete')
            waiter.wait(
                StackName=stack_name
            )
            print("Stack create complete")
            print("Get SG")
            sg_id = self.cfn.describe_stack_resource(
                StackName=stack_name,
                LogicalResourceId='InstanceSecurityGroup'
            )
            print("SG ID to delete - " +
                  sg_id['StackResourceDetail']['PhysicalResourceId'])
            response = self.ec2.delete_security_group(
                GroupId=sg_id['StackResourceDetail']['PhysicalResourceId'],
            )
            print("SG deleted")
            print("Updating testcase1 stack")
            response = self.cfn.update_stack(
                StackName=stack_name,
                TemplateURL='https://muralikl.s3.amazonaws.com/testcase1/updated_stack.yml'
            )
            # get the stack status and wait until its in UPDATE_ROLLBACK_FAILED state
            if self.helpers.wait_until_urf(stack_name) == True:
                print("Stack must be in UPDATE_ROLLBACK_FAILED")
            cfn_command = subprocess.run(['cfn-cur', '-s', stack_arn], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, universal_newlines=True)
            if cfn_command.returncode == 0:
                print("Got CLI Command")
                print("executing")
                print(cfn_command.stdout.strip())
                result = subprocess.run(cfn_command.stdout.strip().split(), stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                print(result.returncode)
            waiter = self.cfn.get_waiter('stack_update_complete')
            waiter.wait(
                StackName=stack_name
            )
            print("stack in URC")
        except Exception as err:
            print(err)
        else:
            print("Nothing went wrong")
