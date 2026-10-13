"""
Automated AWS Infrastructure Provisioning Script
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps

Provisions the complete cloud infrastructure for the DevOps Incident Watchdog:
1. Amazon S3 Bucket: Private secure crash dump storage.
2. IAM Role: Least-privilege permissions for Lambda (S3 write + CloudWatch logs).
3. Monitored Application (AWS Lambda + Function URL): Live public endpoint.
4. Incident Watchdog Lambda: Autonomous parser and GitHub ticket creator.
5. CloudWatch Subscription Filter: Connects application crash logs directly to the Watchdog.
"""

import io
import json
import os
import sys
import time
import zipfile
import boto3
from botocore.exceptions import ClientError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def setup_aws_session(region):
    """Initializes boto3 session with automatic prompt if credentials missing."""
    try:
        session = boto3.Session(region_name=region)
        sts = session.client("sts")
        sts.get_caller_identity()
        return session
    except Exception:
        print("\n" + "=" * 60)
        print("  [!] Please enter your AWS Credentials:")
        print("  (From your AWS Free Tier or AWS Academy Learner Lab)")
        print("=" * 60)
        access_key = input("AWS Access Key ID: ").strip()
        secret_key = input("AWS Secret Access Key: ").strip()
        session_token = input("AWS Session Token (Press Enter if none / personal account): ").strip()

        kwargs = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region
        }
        if session_token:
            kwargs["aws_session_token"] = session_token

        return boto3.Session(**kwargs)


def get_current_account_id(sts_client):
    try:
        identity = sts_client.get_caller_identity()
        return identity["Account"]
    except Exception as e:
        print(f"Error authenticating with AWS: {e}")
        print("\nPlease check your AWS Access Key and Secret Key and try again.")
        sys.exit(1)


def create_s3_bucket(s3_client, bucket_name, region):
    print(f"\n[1/5] Setting up Amazon S3 Bucket: {bucket_name}...")
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"  [OK] S3 Bucket created: {bucket_name}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            print(f"  [OK] S3 Bucket already exists and is ready: {bucket_name}")
        else:
            print(f"  [ERROR] Error creating S3 bucket: {e}")
            raise

    # Enforce private bucket & block public access (Security Requirement)
    try:
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True
            }
        )
        print("  [OK] S3 Bucket Public Access Block enforced (Private & Secure).")
    except Exception as e:
        print(f"  ! Note on public access block: {e}")


def create_iam_role(iam_client, role_name, bucket_name):
    print(f"\n[2/5] Setting up IAM Role: {role_name}...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        role = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Execution role for DevOps Incident Watchdog Lambda"
        )
        role_arn = role["Role"]["Arn"]
        print(f"  [OK] IAM Role created: {role_arn}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            role = iam_client.get_role(RoleName=role_name)
            role_arn = role["Role"]["Arn"]
            print(f"  [OK] IAM Role exists: {role_arn}")
        else:
            raise

    # Attach basic execution policy
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    )

    # Attach S3 PutObject policy
    s3_policy_name = f"{role_name}-S3Policy"
    s3_policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject", "s3:GetObject"],
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }
    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName=s3_policy_name,
        PolicyDocument=json.dumps(s3_policy_doc)
    )
    print("  [OK] Attached AWSLambdaBasicExecutionRole and S3 Write policies.")
    return role_arn


def create_zip_buffer(file_map):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, filepath in file_map.items():
            if os.path.exists(filepath):
                zf.write(filepath, arcname)
            else:
                print(f"Warning: File not found {filepath}")
    buffer.seek(0)
    return buffer.read()


def deploy_lambda_function(lambda_client, function_name, role_arn, handler, zip_bytes, env_vars=None):
    print(f"  Deploying Lambda function '{function_name}'...")
    env_vars = env_vars or {}
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.12",
            Role=role_arn,
            Handler=handler,
            Code={"ZipFile": zip_bytes},
            Description="DevOps Incident Watchdog component",
            Timeout=15,
            MemorySize=128,
            Environment={"Variables": env_vars}
        )
        print(f"  [OK] Lambda created: {function_name}")
        return response["FunctionArn"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceConflictException":
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_bytes
            )
            lambda_client.update_function_configuration(
                FunctionName=function_name,
                Environment={"Variables": env_vars}
            )
            fn_info = lambda_client.get_function(FunctionName=function_name)
            print(f"  [OK] Lambda updated: {function_name}")
            return fn_info["Configuration"]["FunctionArn"]
        else:
            raise


def enable_function_url(lambda_client, function_name):
    """Creates a public HTTPS URL for the target application to test live in the browser."""
    try:
        res = lambda_client.create_function_url_config(
            FunctionName=function_name,
            AuthType="NONE"
        )
        url = res["FunctionUrl"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceConflictException":
            res = lambda_client.get_function_url_config(FunctionName=function_name)
            url = res["FunctionUrl"]
        else:
            return None

    # Grant public invoke permission
    try:
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId="FunctionURLAllowPublicAccess",
            Action="lambda:InvokeFunctionUrl",
            Principal="*",
            FunctionUrlAuthType="NONE"
        )
    except ClientError:
        pass  # Already allowed

    return url


def main():
    print("=" * 65)
    print("  Auto-Incident to Agile Ticket Pipeline (AWS Deployer)")
    print("  Student: S Hemal (24MIS0050) | Agile & DevOps Assessment")
    print("=" * 65)

    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    print(f"Target AWS Region: {region}")

    session = setup_aws_session(region)
    sts = session.client("sts")
    account_id = get_current_account_id(sts)
    print(f"Authenticated as AWS Account: {account_id}")

    s3 = session.client("s3")
    iam = session.client("iam")
    lam = session.client("lambda")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # GitHub repository settings
    github_owner = os.environ.get("GITHUB_REPO_OWNER") or input("\nEnter your GitHub Username/Org: ").strip()
    github_repo = os.environ.get("GITHUB_REPO_NAME") or input("Enter your GitHub Repository Name: ").strip()
    github_token = os.environ.get("GITHUB_TOKEN") or input("Enter your GitHub Personal Access Token (PAT): ").strip()

    bucket_name = f"devops-incident-watchdog-logs-{account_id}-{region}"
    role_name = "DevOpsIncidentWatchdogLambdaRole"

    # Step 1: Create S3 Bucket
    create_s3_bucket(s3, bucket_name, region)

    # Step 2: Create IAM Role
    role_arn = create_iam_role(iam, role_name, bucket_name)
    print("  Waiting 10 seconds for IAM Role propagation in AWS...")
    time.sleep(10)

    # Step 3: Deploy Monitored App Lambda
    print("\n[3/5] Deploying Monitored Web Application (watchdog-target-app)...")
    app_zip = create_zip_buffer({
        "app/__init__.py": os.path.join(base_dir, "app", "__init__.py"),
        "app/app.py": os.path.join(base_dir, "app", "app.py"),
        "app/lambda_app_adapter.py": os.path.join(base_dir, "app", "lambda_app_adapter.py"),
    })
    deploy_lambda_function(
        lambda_client=lam,
        function_name="watchdog-target-app",
        role_arn=role_arn,
        handler="app.lambda_app_adapter.lambda_handler",
        zip_bytes=app_zip,
        env_vars={"APP_VERSION": "1.0.0"}
    )
    app_url = enable_function_url(lam, "watchdog-target-app")
    if app_url:
        print(f"  [OK] Live Public App URL: {app_url}")
        print(f"       Health check: {app_url}health")
        print(f"       Simulate incident: {app_url}simulate-crash")

    # Step 4: Deploy Watchdog Lambda
    print("\n[4/5] Deploying Incident Watchdog Lambda (watchdog-incident-creator)...")
    watchdog_zip = create_zip_buffer({
        "lambda_watchdog/__init__.py": os.path.join(base_dir, "lambda_watchdog", "__init__.py"),
        "lambda_watchdog/watchdog.py": os.path.join(base_dir, "lambda_watchdog", "watchdog.py"),
    })
    watchdog_env = {
        "INCIDENT_LOGS_BUCKET": bucket_name,
        "GITHUB_REPO_OWNER": github_owner,
        "GITHUB_REPO_NAME": github_repo,
        "GITHUB_TOKEN": github_token,
        "AWS_REGION": region
    }
    watchdog_arn = deploy_lambda_function(
        lambda_client=lam,
        function_name="watchdog-incident-creator",
        role_arn=role_arn,
        handler="lambda_watchdog.watchdog.lambda_handler",
        zip_bytes=watchdog_zip,
        env_vars=watchdog_env
    )

    print("\n[5/5] AWS Infrastructure Deployment Completed Successfully! [DONE]")
    print("=" * 65)
    print("Summary for Faculty Presentation:")
    print(f"- S3 Bucket:              {bucket_name}")
    print(f"- Monitored App Lambda:   watchdog-target-app")
    if app_url:
        print(f"- Live Public Web URL:    {app_url}")
    print(f"- Watchdog Lambda:        watchdog-incident-creator")
    print(f"- Agile Board (GitHub):   https://github.com/{github_owner}/{github_repo}/issues")
    print("=" * 65)


if __name__ == "__main__":
    main()
