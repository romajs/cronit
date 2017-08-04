#!/usr/bin/env python
import boto3, sys

cronit_lambda_id = sys.argv[1]
cronit_lambda_arn = sys.argv[2]

ec2_client = boto3.client('ec2')
events_client = boto3.client('events')

def get_ec2_instances():
	return ec2_client.describe_instances(Filters=[
		{'Name': 'tag-key', 'Values': ['cronit:start']},
		{'Name': 'tag-key', 'Values': ['cronit:stop']}
	])

def put_event_rule(nature, instance_id, cron_expression, i):
	event_rule_name = 'cronit_%s_%s_%d' % (instance_id, nature, i)
	event_rule = events_client.put_rule(Name=event_rule_name,
		Description='%ss the instance "%s" at "cron(%s)"' % (nature.title(), instance_id, cron_expression),
		ScheduleExpression='cron(%s)' % cron_expression,
		State='ENABLED')
	print event_rule_name, event_rule
	return event_rule_name, event_rule

def put_event_target(event_rule_name):
	event_target = events_client.put_targets(Rule=event_rule_name, Targets=[{'Id': cronit_lambda_id, 'Arn': cronit_lambda_arn}])
	print event_target
	return event_target

if __name__ == "__main__":

	ec2_instances = get_ec2_instances()

	event_rules = []

	for reservation in ec2_instances['Reservations']:

		for ec2_instance in reservation['Instances']:

			item = (
				ec2_instance['InstanceId'],
				map(lambda tag: tag['Value'], filter(lambda tag: tag['Key'] == 'cronit:start', ec2_instance['Tags'])),
				map(lambda tag: tag['Value'], filter(lambda tag: tag['Key'] == 'cronit:stop', ec2_instance['Tags']))
			)

			print item

			for i, cron_expression in enumerate(item[1]):
				event_rule_name, event_rule = put_event_rule('start', item[0], cron_expression, i)
				put_event_target(event_rule_name)

			for i, cron_expression in enumerate(item[2]):
				event_rule_name, event_rule = put_event_rule('stop', item[0], cron_expression, i)
				put_event_target(event_rule_name)

			print