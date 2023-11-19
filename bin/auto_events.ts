#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { DeltaBracketStack } from '../lib/stacks/delta_bracket_v1/delta_bracket_stack';

const app = new cdk.App();

const stage = process.env.STAGE;
const ubi_auth = process.env.UBI_AUTH;
let club_id: number;
let campaign_id: number;
let event_name: string;


// TODO manual approval is not avaiable YET in codecatalyst so it will go straight to prod, rip
if (stage == 'dev' || stage == 'beta') {
    club_id = 69352; // Auto Events Staging
    campaign_id = 55190; // DO NOT MODIFY
    event_name = "Delta Bracket Test";
} else if (stage == 'prod') {
    club_id = 58261; // Auto Events
    campaign_id = 55644; // Delta Bracket Beta
    event_name = "Delta Bracket";
} else {
    console.log('Environment variable unsupported, expected one of dev|beta|prod');
    process.exit(1);
}

if (!ubi_auth) {
    console.log('Environment variable UBI_AUTH is required');
    process.exit(1);
}

new DeltaBracketStack(app, `DeltaBracketStack-${stage}`, {
    stage: stage,
    event_name: event_name,
    club_id: club_id,
    campaign_id: campaign_id,
    ubi_auth: ubi_auth,
})