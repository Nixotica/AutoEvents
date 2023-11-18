import { Stack, StackProps } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export interface DeltaBracketStackProps extends StackProps {
    
}

export class DeltaBracketStack extends Stack {
    constructor(scope: Construct, id: string, props?: DeltaBracketStackProps) {
        super(scope, id, props);

        // Create lambda which handles event actions
        const lambda = new Function(this, "DeltaBracketEventActionsLambda", {
            runtime: Runtime.PYTHON_3_11,
            code: Code.fromAsset("./lib/lambdas/src/"),
            handler: "delta_bracket_v1.lambda_handler.handler",
        });

        // Create Rule which calls create event at the given schedule
        // TODO 

        // Create Rule which calls delete event at the given schedule
        // TODO
    }
}