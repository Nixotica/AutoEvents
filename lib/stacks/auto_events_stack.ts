 import { Stack, StackProps } from 'aws-cdk-lib';
import { Bucket, BucketAccessControl, BucketEncryption } from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class AutoEventsStack extends Stack {
  public readonly secretsBucket: Bucket;

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Make a bucket to store encrypted data in
    // YOU ARE RESPONSIBLE FOR UPLOADING SECRETS HERE MANUALLY (e.g. UBI_AUTH)
    this.secretsBucket = new Bucket(this, "AutoEventsSecretsBucket", {
      encryption: BucketEncryption.S3_MANAGED,
      accessControl: BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
    });
  }
}
