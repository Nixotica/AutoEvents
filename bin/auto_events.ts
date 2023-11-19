#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { DeltaBracketStack } from '../lib/stacks/delta_bracket_v1/delta_bracket_stack';

const app = new cdk.App();

const stage = process.env.STAGE;
const ubi_auth = process.env.UBI_AUTH;


if (!ubi_auth) {
    console.log('Environment variable UBI_AUTH is required');
    process.exit(1);
}

// For local testing, make sure you've run `export STAGE=dev`
if (stage == 'dev') {
    new DeltaBracketStack(app, 'DeltaBracketStack-dev', {
        stage: 'dev',
        event_name: "Delta Bracket Dev Test",
        club_id: 69352, // "Auto Events Staging"
        campaign_id: 55190, // "DO NOT MODIFY"
        ubi_auth: ubi_auth,
    });
} else {
    new DeltaBracketStack(app, 'DeltaBracketStack-prod', {
        stage: 'prod',
        event_name: "Delta Bracket Beta",
        club_id: 58261, // "Auto Events"
        campaign_id: 55644, // "Delta Bracket Beta"
        ubi_auth: ubi_auth,
    })
}