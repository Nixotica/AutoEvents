#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { DeltaBracketStack } from '../lib/stacks/delta_bracket_v1/delta_bracket_stack';
import { AutoEventsStack } from '../lib/stacks/auto_events_stack';
import { PanAmericanOfTheDayStack } from '../lib/stacks/pan_american_of_the_day/pan_american_of_the_day_stack';

const app = new cdk.App();
const env = {
    account: "115984396435"
}

// Common resources stack
const resourcesStack = new AutoEventsStack(app, 'AutoEventsResourcesStack', {env: env});

// For local testing, make sure you've run `export STAGE=dev`
if (process.env.STAGE == 'dev') {
    new DeltaBracketStack(app, 'DeltaBracketStack-dev', {
        env: env,
        stage: 'dev',
        event_name: "DBDevTest",
        club_id: 69352, // "Auto Events Staging"
        campaign_id: 55190, // "DO NOT MODIFY"
        secrets_bucket: resourcesStack.secretsBucket,
    });

    new PanAmericanOfTheDayStack(app, 'PanAmericanOfTheDayStack-dev', {
       env: env,
       stage: 'dev',
       event_name: "PAOTDDevTest",
       event_club_id: 69352, // "Auto Events Staging"
       maps_club_id: 69352, // "Auto Events Staging"
       campaign_id: 55190, // "DO NOT MODIFY"
       secrets_bucket: resourcesStack.secretsBucket,
    });
} else {
    new DeltaBracketStack(app, 'DeltaBracketStack-beta', {
        env: env,
        stage: 'beta',
        event_name: "DBBetaTest",
        club_id: 69352, // "Auto Events Staging"
        campaign_id: 55190, // "DO NOT MODIFY"
        secrets_bucket: resourcesStack.secretsBucket,
    });
    new DeltaBracketStack(app, 'DeltaBracketStack-prod', {
        env: env,
        stage: 'prod',
        event_name: "Delta Bracket",
        club_id: 58261, // "Auto Events"
        campaign_id: 55644, // "Delta Bracket Beta"
        secrets_bucket: resourcesStack.secretsBucket,
    });

    new PanAmericanOfTheDayStack(app, 'PanAmericanOfTheDayStack-beta', {
        env: env,
        stage: 'beta',
        event_name: "PAOTDBetaTest",
        event_club_id: 69352, // "Auto Events Staging"
        maps_club_id: 69352, // "Auto Events Staging"
        campaign_id: 55190, // "DO NOT MODIFY"
        secrets_bucket: resourcesStack.secretsBucket,
    });
    new PanAmericanOfTheDayStack(app, 'PanAmericanOfTheDayStack-prod', {
        env: env,
        stage: 'prod',
        event_name: "PAOTD",
        event_club_id: 58261, // "Auto Events"
        maps_club_id: 68298, // "NCSA Trackmania"
        campaign_id: 58789, // "PATC S2 Campaign" TODO switch to a rotating campaign
        secrets_bucket: resourcesStack.secretsBucket,
    });
}