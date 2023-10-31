import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import * as AutoEvents from '../lib/auto_events-stack';

test('Rule and Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new AutoEvents.AutoEventsStack(app, 'MyTestStack');
  // THEN

  const template = Template.fromStack(stack);

  template.resourceCountIs('AWS::Lambda::Function', 1);
  template.resourceCountIs('AWS::Events::Rule', 1);
});
