import boto3
import time

# Set your AWS credentials and region
aws_access_key_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
aws_secret_access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
region_name = 'ap-south-1'

# Create an EC2 client
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                   region_name=region_name)

# Specify the details for your EC2 instances
instance_params = {
    'ImageId': 'ami-0d3f444bc76de0a79',  # Replace with the desired AMI ID
    'InstanceType': 't2.micro',  # Replace with the desired instance type
    'KeyName': 'mylocalmumbai',  # Replace with your key pair name
    'MinCount': 1,
    'MaxCount': 3,
}

# Launch the EC2 instances
response = ec2.run_instances(**instance_params)

# Get the instance IDs
instance_ids = [instance['InstanceId'] for instance in response['Instances']]
print(f"Launched instances: {', '.join(instance_ids)}")

# Wait for the instances to be in the 'running' state
print("Waiting for instances to be in the 'running' state...")
ec2.get_waiter('instance_running').wait(InstanceIds=instance_ids)

print("Instances are now in the 'running' state.")

# Retrieve details about the instances
instance_details = ec2.describe_instances(InstanceIds=instance_ids)

# Print instance details including name and public IP
for reservation in instance_details['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_name = [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'][
            0] if 'Tags' in instance else ''
        public_ip = instance.get('PublicIpAddress', 'N/A')

        print(f"Instance ID: {instance_id}, Name: {instance_name}, Public IP: {public_ip}")
