import boto3

INSTANCE_ID = "i-016f5ae6fe0692b68"
REGION = "ap-south-1"

cloudwatch = boto3.client("cloudwatch", region_name=REGION)

response = cloudwatch.put_metric_alarm(
    AlarmName="StreamingApp-EC2-High-CPU",
    AlarmDescription="Alert when EC2 CPU utilization exceeds 80 percent",
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[
        {
            "Name": "InstanceId",
            "Value": INSTANCE_ID
        }
    ],
    Statistic="Average",
    Period=300,
    EvaluationPeriods=2,
    Threshold=80.0,
    ComparisonOperator="GreaterThanThreshold",
    TreatMissingData="notBreaching"
)

print("CloudWatch alarm created successfully!")
print("Alarm: StreamingApp-EC2-High-CPU")
