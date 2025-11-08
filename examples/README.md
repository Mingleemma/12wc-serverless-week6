# EC2 Instance Management Lambda Functions

AWS Lambda functions to start and stop EC2 instances with optional SNS notifications.

## Files

- `start.py` - Starts EC2 instance and waits for public IP assignment
- `stop.py` - Stops EC2 instance

## Configuration

### Required Environment Variables
- `INSTANCE_ID` - EC2 instance ID to manage

### Optional Environment Variables
- `AWS_REGION` - AWS region (defaults to `us-east-1`)
- `SNS_TOPIC_ARN` - SNS topic ARN for notifications (optional)

## Features

- **start.py**: Waits up to 120 seconds for public IP assignment
- **stop.py**: Immediately stops the specified instance
- **SNS Notifications**: Optional notifications when SNS_TOPIC_ARN is configured
- **Multi-region Support**: Works in any AWS region

## Required IAM Permissions

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "*"
        }
    ]
}
```

## Setup Example

```bash
# Set environment variables
export INSTANCE_ID="i-1234567890abcdef0"
export AWS_REGION="us-west-2"
export SNS_TOPIC_ARN="arn:aws:sns:us-west-2:123456789012:EC2Notifications"
```

## Deployment

1. Create Lambda functions with the code
2. Set environment variables
3. Attach IAM role with required permissions
4. Configure triggers (EventBridge, API Gateway, etc.)

## Triggers

- **CloudWatch Events/EventBridge** - Schedule-based automation
- **API Gateway** - HTTP endpoint control
- **Manual invocation** - Direct Lambda execution