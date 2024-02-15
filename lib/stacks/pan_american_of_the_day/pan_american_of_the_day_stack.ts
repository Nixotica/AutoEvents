import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";
import { Duration, Stack, StackProps, TimeZone } from "aws-cdk-lib";
import { Rule, RuleTargetInput, Schedule } from "aws-cdk-lib/aws-events";
import { LambdaFunction } from "aws-cdk-lib/aws-events-targets";
import { Runtime } from "aws-cdk-lib/aws-lambda";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";

export interface PanAmericanOfTheDayStackProps extends StackProps {
    /** The stage of this stack (dev, beta, prod). */
    stage: string;

    /** The name of the event. */
    event_name: string;

    /** The club in which to host the event. */
    event_club_id: number,

    /** The club from which to get the campaign containing maps to use. */
    maps_club_id: number,

    /** The campaign containing the map pool to use. */
    campaign_id: number,

    /** A common Auto Events bucket containing secrets to give lambdas read access to. */
    secrets_bucket: Bucket,

    /** Indicates if we should post notifications to discord. */
    notify: boolean,
}

export class PanAmericanOfTheDayStack extends Stack {
    constructor(scope: Construct, id: string, props: PanAmericanOfTheDayStackProps) {
        super(scope, id, props);

        // Create an s3 bucket to hold event information between lambda invocations
        const bucket = new Bucket(this, "PAOTD_Event_Bucket", {
            bucketName: `paotd-event-${props.stage.toLowerCase()}`,
        });

        // Create lambda which handles event actions (creation, deletion, notifications, etc)
        const lambda = new PythonFunction(this, "PAOTD_Event_Actions_Lambda", {
            runtime: Runtime.PYTHON_3_10,
            entry: "./lib/lambdas/src/",
            index: "lambda_handler.py",
            handler: "handler",
            timeout: Duration.seconds(30),
            // These variables should match those in pan_american_of_the_day/src/environment.py
            environment: {
                "EVENT_NAME": props.event_name,
                "EVENT_CLUB_ID": props.event_club_id.toString(),
                "MAPS_CLUB_ID": props.maps_club_id.toString(),
                "CAMPAIGN_ID": props.campaign_id.toString(),
                "STORAGE_BUCKET_NAME": bucket.bucketName,
                "SECRETS_BUCKET_NAME": props.secrets_bucket.bucketName,
            },
        });


        if (props.notify) {
            // Create Rule which calls notify event at the given schedule
            const notifyEventRule = new Rule(this, "PAOTD_Notify_Event_Rule", {
                schedule: Schedule.cron({ // TODO https://github.com/aws/aws-cdk/issues/21181
                    hour: "3",
                    minute: "45",
                })
            });

            // Call lambda with appropriate payload for notify
            notifyEventRule.addTarget(new LambdaFunction(lambda, {
                event: RuleTargetInput.fromObject({
                    "event_name": "paotd",
                    "action": "notify",
                }),
            }));
        }
        
        // TODO call notify of participants and winners at hour 5:30

        // Create Rule which calls delete event at the given schedule
        const deleteEventRule = new Rule(this, "PAOTD_Delete_Event_Rule", {
            schedule: Schedule.cron({
                hour: "6",
                minute: "0",
            }),
        });

        // Create Rule which calls create event at the given schedule
        const createEventRule = new Rule(this, "PAOTD_Create_Event_Rule", {
            schedule: Schedule.cron({
                hour: "7",
                minute: "0",
            }),
        });

        // Call lambda with appropriate payload for create and delete
        deleteEventRule.addTarget(new LambdaFunction(lambda, {
            event: RuleTargetInput.fromObject({
                "event_name": "paotd",
                "action": "delete",
            }),
        }));
        createEventRule.addTarget(new LambdaFunction(lambda, {
            event: RuleTargetInput.fromObject({
                "event_name": "paotd",
                "action": "create",
            }),
        }));

        // Grant lambda permissions to read/write to the bucket
        bucket.grantReadWrite(lambda);

        // Give it access to read secrets from secrets bucket
        props.secrets_bucket.grantRead(lambda);
    }
}