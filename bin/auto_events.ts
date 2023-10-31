#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { AutoEventsStack } from '../lib/auto_events-stack';

const app = new cdk.App();
new AutoEventsStack(app, 'AutoEventsStack');
