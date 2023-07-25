import os
import json
import boto3


def lambda_handler(event, _):
    print("Triggered getTextFromS3PDF event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    try:
        textract = boto3.client("textract")
        textract.start_document_analysis(
            DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}},
            JobTag=key + "_Job",
            FeatureTypes=["TABLES"],
            NotificationChannel={
                "RoleArn": os.environ["SNSROLEARN"],
                "SNSTopicArn": os.environ["SNSTOPIC"],
            },
        )

        return "Triggered PDF Processing for " + key
    except Exception as e:
        print(e)
        print(
            "Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.".format(
                key, bucket
            )
        )
        raise e
