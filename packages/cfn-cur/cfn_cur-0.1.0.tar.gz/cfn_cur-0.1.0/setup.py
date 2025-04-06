from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cfn-cur',
    version='0.1.0',
    description='A tool to generate CLI Command to continue update rollback of CloudFormation stacks',
    author='S Murali Krishnan',
    author_email="mrlikrsh@gmail.com",
    url="https://github.com/mrlikl/continue-update-rollback",
    packages=['continue_update_rollback'],
    entry_points={
        'console_scripts': [
            'cfn-cur = continue_update_rollback.app:main'
        ]
    },
    install_requires=[
        'boto3',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
)
