import boto3
import time
from datetime import datetime
import os
instances = os.environ['INSTANCE_ID']
instances = [instances]
region = 'us-west-2'
# instances = ['i-08dede33e781b63b2']
sns_topic_arn = 'arn:aws:sns:us-west-2:801387502566:EC2StartNotification'  # Replace with your SNS topic ARN
ec2 = boto3.client('ec2', region_name=region)
sns = boto3.client('sns', region_name=region)

def lambda_handler(event, context):
    # Record the start time
    start_time = datetime.utcnow()
    print(f'Starting instance(s): {instances} at {start_time.strftime("%Y-%m-%d %H:%M:%S UTC")}')
    
    # Start the instance
    ec2.start_instances(InstanceIds=instances)
    
    # Initialize the public_ip variable
    public_ip = None
    port = 5001
    max_wait_time = 120  # seconds
    wait_interval = 5  # seconds
    
    # Loop until the public IP is assigned or max wait time is reached
    elapsed_time = 0
    while public_ip is None and elapsed_time < max_wait_time:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        
        # Retrieve the instance details
        instance_info = ec2.describe_instances(InstanceIds=instances)
        
        # Try to get the public IP address
        public_ip = instance_info['Reservations'][0]['Instances'][0].get('PublicIpAddress')
        
        # Log a message to indicate the loop is running
        print("Waiting for public IP assignment...")

    # Log the final message with the public IP and start time
    if public_ip:
        dashboard_url = f"{public_ip}"
        notification_message = f"Hello there, \n\nKindly head to this link - {dashboard_url} to access the Dashboard."

        # notification_message = f"Instance Started:\n\n{message}"
        notify = f'Instance Started. Details: {notification_message}'
        print(notify)
        return notify
    else:
        notification_message = f'Instance started at {start_time.strftime("%Y-%m-%d %H:%M:%S UTC")} but no public IP assigned within {max_wait_time} seconds.'
        print(notification_message)
        print('Test Componets')

    # #Publish the message to the SNS topic
    # sns.publish(
    #     TopicArn=sns_topic_arn,
    #     Message=notification_message,
    #     Subject='EC2 Instance Start Notification'
    # )