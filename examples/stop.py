import boto3
import os

# Environment variables
instances = [os.environ['INSTANCE_ID']]
region = os.environ.get('AWS_REGION', 'us-east-1')
sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')

ec2 = boto3.client('ec2', region_name=region)
sns = boto3.client('sns', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    message = {
            "InstanceId": instances
        }
    notification_message = f"Instance Stopped {message}"
    print('stopped your instances: ' + str(instances))
    
    # Publish the message to the SNS topic if configured
    if sns_topic_arn:
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=notification_message,
            Subject='EC2 Instance Stop Notification'
        )
    
    return notification_message