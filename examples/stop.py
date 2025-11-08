import boto3
import os

region = 'us-west-2'
# instances = os.environ['INSTANCE_ID']
# instances = [instances]
instances = ['i-08dede33e781b63b2']
ec2 = boto3.client('ec2', region_name=region)
sns = boto3.client('sns', region_name=region)
sns_topic_arn = 'arn:aws:sns:us-west-2:801387502566:EC2StartNotification'

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    message = {
            "InsanceId": instances
        }
    notification_message = f"Instance Stopped {message}"
    print('stopped your instances: ' + str(instances))
    return notification_message

    
    # Publish the message to the SNS topic
    sns.publish(
        TopicArn=sns_topic_arn,
        Message=notification_message,
        Subject='EC2 Instance Start Notification'
    )