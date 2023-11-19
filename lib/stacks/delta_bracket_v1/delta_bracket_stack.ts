import { Stack, StackProps } from "aws-cdk-lib";
import { Rule, RuleTargetInput, Schedule } from "aws-cdk-lib/aws-events";
import { LambdaFunction } from "aws-cdk-lib/aws-events-targets";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";

export interface DeltaBracketStackProps extends StackProps {
    /** The stage of this stack (dev, beta, prod, etc) */
    stage: string,

    /** The name of the event. */
    event_name: string,
    
    /** The club in which to host the event. */
    club_id: number,

    /** The campaign containing the map pool to use for the event. */
    campaign_id: number,

    /** The UBI authorization (Basic <user:pass base 64>) to use with the API. */
    ubi_auth: string,
}

export class DeltaBracketStack extends Stack {
    constructor(scope: Construct, id: string, props: DeltaBracketStackProps) {
        super(scope, id, props);

        // Create an s3 bucket to hold event information
        const bucket = new Bucket(this, "DeltaBracketEventBucket", {
            bucketName: `delta-bracket-event-${props.stage.toLowerCase()}`,
        });

        // Create lambda which handles event actions
        const lambda = new Function(this, "DeltaBracketEventActionsLambda", {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset("./lib/lambdas/src/"),
            handler: "delta_bracket_v1.lambda_handler.handler",
            environment: {
                "EVENT_NAME": props.event_name,
                "UBI_AUTH": props.ubi_auth,
                "CLUB_ID": props.club_id.toString(),
                "CAMPAIGN_ID": props.campaign_id.toString(),
                "STORAGE_BUCKET_NAME": bucket.bucketName,
            }
        });

        // Create Rule which calls create event at the given schedule 
        const createEventRule = new Rule(this, "DeltaBracketEventCreateRule", {
            schedule: Schedule.cron({
                weekDay: "MON",
                hour: "12",
                minute: "0"
            })
        });

        // Create Rule which calls delete event at the given schedule
        const deleteEventRule = new Rule(this, "DeltaBracketEventDeleteRule", {
            schedule: Schedule.cron({
                weekDay: "SUN",
                hour: "12",
                minute: "0"
            })
        });

        // Call lambda with appropriate payload for create and delete
        createEventRule.addTarget(new LambdaFunction(lambda, {
            event: RuleTargetInput.fromObject({
                "action": "create"
            })
        }));
        deleteEventRule.addTarget(new LambdaFunction(lambda, {
            event: RuleTargetInput.fromObject({
                "action": "delete"
            })
        }));

        // Grant lambda permissions to read/write to the bucket
        bucket.grantReadWrite(lambda);
    }
}