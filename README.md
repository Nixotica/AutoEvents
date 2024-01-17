# Welcome to your CDK TypeScript project

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`AutoEventsStack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## Development

1. Run `pip install -r requirements.txt`.
2. Set environment variables `UBI_AUTH`, `EVENT_NAME`, `CLUB_ID`, `CAMPAIGN_ID`, `EVENT_CLUB_ID`, `MAPS_CLUB_ID`, `SECRETS_BUCKET_NAME`, and `STORAGE_BUCKET_NAME` (these are all necessary for integration tests). Make sure that separate storage and secret s3 buckets exist in your AWS account. 
3. Run `aws configure` with your public and secret AWS access key. 
4. Set environment variable `STAGE` to "dev", as this will be used for deploying your personal stack to test with.
5. Start using the Useful Commands to play around! 
