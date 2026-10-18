"""
Direct AWS Infrastructure Deployment Script
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps
"""

import io
import json
import os
import sys
import time
import zipfile
import boto3
from botocore.exceptions import ClientError

REGION = "ap-southeast-2"
ACCOUNT_ID = "401537512022"
BUCKET_NAME = f"devops-incident-watchdog-logs-{ACCOUNT_ID}"
ROLE_NAME = "DevOpsIncidentWatchdogLambdaRole"

AWS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

session = boto3.Session(
    aws_access_key_id=AWS_KEY or None,
    aws_secret_access_key=AWS_SECRET or None,
    region_name=REGION
)

s3 = session.client("s3")
iam = session.client("iam")
lam = session.client("lambda")
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print("=" * 65)
print("  Deploying DevOps Incident Watchdog to AWS")
print(f"  Account: {ACCOUNT_ID} | Region: {REGION}")
print("=" * 65)

# 1. Block public access on S3 bucket
print("\n[1/4] Securing Amazon S3 Bucket...")
try:
    s3.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        }
    )
    print("  [OK] Private S3 Bucket access enforced.")
except Exception as e:
    print(f"  [Note] S3 access block: {e}")

# 2. Setup IAM Role
print("\n[2/4] Setting up IAM Execution Role...")
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

try:
    role = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="Execution role for DevOps Incident Watchdog"
    )
    role_arn = role["Role"]["Arn"]
    print(f"  [OK] IAM Role created: {role_arn}")
except ClientError as e:
    if e.response["Error"]["Code"] == "EntityAlreadyExists":
        role = iam.get_role(RoleName=ROLE_NAME)
        role_arn = role["Role"]["Arn"]
        print(f"  [OK] IAM Role already exists: {role_arn}")
    else:
        raise

# Attach basic execution role
iam.attach_role_policy(
    RoleName=ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

# Attach S3 PutObject policy
s3_policy_name = f"{ROLE_NAME}-S3Access"
s3_policy_doc = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:PutObject", "s3:GetObject"],
        "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
    }]
}
iam.put_role_policy(
    RoleName=ROLE_NAME,
    PolicyName=s3_policy_name,
    PolicyDocument=json.dumps(s3_policy_doc)
)
print("  [OK] IAM Permissions attached (S3 Write + CloudWatch Logging).")

print("  Waiting 10 seconds for IAM Role propagation in AWS...")
time.sleep(10)


def make_zip(file_map):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, fpath in file_map.items():
            if os.path.exists(fpath):
                zf.write(fpath, arcname)
    buf.seek(0)
    return buf.read()


# 3. Deploy Target App Lambda
print("\n[3/4] Deploying Monitored Web Application (watchdog-target-app)...")
index_html = os.path.join(base_dir, "templates", "index.html")
app_zip = make_zip({
    "app/lambda_app_adapter.py": os.path.join(base_dir, "app", "lambda_app_adapter.py"),
    "app/templates/index.html": index_html,
    "templates/index.html": index_html,
    "index.html": index_html,
})

try:
    lam.create_function(
        FunctionName="watchdog-target-app",
        Runtime="python3.12",
        Role=role_arn,
        Handler="app.lambda_app_adapter.lambda_handler",
        Code={"ZipFile": app_zip},
        Description="DevOps Incident Watchdog Target Service",
        Timeout=15,
        MemorySize=128
    )
    print("  [OK] Lambda function created: watchdog-target-app")
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceConflictException":
        lam.update_function_code(FunctionName="watchdog-target-app", ZipFile=app_zip)
        print("  [OK] Lambda function updated: watchdog-target-app")
    else:
        raise

# Enable Function URL for watchdog-target-app
app_url = None
try:
    res = lam.create_function_url_config(
        FunctionName="watchdog-target-app",
        AuthType="NONE"
    )
    app_url = res["FunctionUrl"]
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceConflictException":
        res = lam.get_function_url_config(FunctionName="watchdog-target-app")
        app_url = res["FunctionUrl"]

# Grant public invoke permission on Function URL
try:
    lam.add_permission(
        FunctionName="watchdog-target-app",
        StatementId="AllowPublicAccessFunctionUrl",
        Action="lambda:InvokeFunctionUrl",
        Principal="*",
        FunctionUrlAuthType="NONE"
    )
except ClientError:
    pass

if app_url:
    print(f"  [OK] Live Public HTTPS URL: {app_url}")

# 4. Deploy Watchdog Lambda
print("\n[4/4] Deploying Incident Watchdog Lambda (watchdog-incident-creator)...")
watchdog_zip = make_zip({
    "lambda_watchdog/watchdog.py": os.path.join(base_dir, "lambda_watchdog", "watchdog.py"),
})

watchdog_env = {
    "INCIDENT_LOGS_BUCKET": BUCKET_NAME,
    "GITHUB_REPO_OWNER": "hemalexe",
    "GITHUB_REPO_NAME": "devopss-incident-watchdog",
}

try:
    lam.create_function(
        FunctionName="watchdog-incident-creator",
        Runtime="python3.12",
        Role=role_arn,
        Handler="lambda_watchdog.watchdog.lambda_handler",
        Code={"ZipFile": watchdog_zip},
        Description="Automated Incident Watchdog Lambda",
        Timeout=15,
        MemorySize=128,
        Environment={"Variables": watchdog_env}
    )
    print("  [OK] Lambda function created: watchdog-incident-creator")
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceConflictException":
        lam.update_function_code(FunctionName="watchdog-incident-creator", ZipFile=watchdog_zip)
        lam.update_function_configuration(FunctionName="watchdog-incident-creator", Environment={"Variables": watchdog_env})
        print("  [OK] Lambda function updated: watchdog-incident-creator")
    else:
        raise

print("\n" + "=" * 65)
print("  [DONE] AWS DEPLOYMENT COMPLETED SUCCESSFULLY!")
print("=" * 65)
print(f"  • Amazon S3 Bucket:      {BUCKET_NAME}")
print("  • App Lambda Function:   watchdog-target-app")
if app_url:
    print(f"  • Live Public HTTPS URL: {app_url}")
print("  • Watchdog Lambda:       watchdog-incident-creator")
print("  • AWS Region:            ap-southeast-2")
print("=" * 65)
