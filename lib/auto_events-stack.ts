import { Stack, StackProps } from 'aws-cdk-lib';
import { Rule, Schedule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction } from 'aws-cdk-lib/aws-events-targets';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export class AutoEventsStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Make a test rule which calls the lambda every 5 minutes
    const callback = new Rule(scope, "TestRule", {
      schedule: Schedule.expression("rate(5 minutes)"), 
    });

    const lambda = new Function(scope, "TestLambda", {
      runtime: Runtime.PYTHON_3_11,
      code: Code.fromAsset("lambda"),
      handler: "test_handler.handler"
    });

    callback.addTarget(new LambdaFunction(lambda));
  }
}
