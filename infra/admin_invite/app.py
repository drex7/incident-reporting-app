import os
import boto3
import json

cognito_client = boto3.client("cognito-idp")
USER_POOL_ID = os.environ["USER_POOL_ID"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        email = body["email"]
        name = body["name"]
        region = body["region"]
        country = body["country"]
        telephone = body["telephone"]
        role = body["role"]

        if role not in ["Admin", "CityOfficial"]:
            return {"statusCode": 400, "body": json.dumps({"error": "Only Admin or CityOfficial allowed"})}

        response = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            TemporaryPassword="TempPass#123",
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "name", "Value": name},
                {"Name": "custom:region", "Value": region},
                {"Name": "custom:country", "Value": country},
                {"Name": "custom:telephone", "Value": telephone},
                {"Name": "email_verified", "Value": "true"}
            ]
        )

        cognito_client.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=email,
            GroupName=role
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"{role} {email} invited successfully"
            })
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
