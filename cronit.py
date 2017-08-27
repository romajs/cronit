#!/usr/bin/env python

import boto3
import click
import logging

logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(threadName)s %(name)s %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger('cronit')

ec2_client = boto3.client('ec2')
events_client = boto3.client('events')

def get_ec2_instances():
	ec2_instances = ec2_client.describe_instances(Filters=[
		{'Name': 'tag-key', 'Values': ['cronit:start']},
		{'Name': 'tag-key', 'Values': ['cronit:stop']}
	])
	return [reservation['Instances'][0] for reservation in ec2_instances['Reservations']]

def put_event_rule(nature, instance_id, cron_expression, i):
	event_rule_name = 'cronit_%s_%s_%d' % (instance_id, nature, i)
	event_rule = events_client.put_rule(Name=event_rule_name,
		Description='%ss the instance "%s" at "cron(%s)"' % (nature.title(), instance_id, cron_expression),
		ScheduleExpression='cron(%s)' % cron_expression,
		State='ENABLED')
	logger.debug('%s: %s' % (event_rule_name, event_rule))
	return event_rule_name, event_rule

def put_event_target(event_rule_name, target_id, target_arn):
	event_target = events_client.put_targets(Rule=event_rule_name, Targets=[{'Id': target_id, 'Arn': target_arn}])
	logger.debug('%s: %s' % (event_rule_name, event_target))
	return event_target

@click.group()
@click.option('--log-level', default='INFO', help='Set logging level')
def cli(log_level):
	logger.setLevel(log_level)
	pass

@cli.command(name='update', help='Update all cronit schedules')
@click.option('--arn', help='Lambda function ARN (arn:aws:lambda:[region]:[id]:function:[name])')
@click.option('--name', default='cronit', help='Lambda function name (default is cronit)')
def update(arn, name):
	logger.debug('AWS Lambda Function ARN: %s' % arn)
	logger.debug('AWS Lambda Function Name: %s' % name)
	ec2_instances = get_ec2_instances()
	logger.info('Found %s EC2 instances with cronit tags' % len(ec2_instances))
	for i, ec2_instance in enumerate(ec2_instances):
		ec2_tuple = (
			ec2_instance['InstanceId'],
			map(lambda tag: tag['Value'], filter(lambda tag: tag['Key'] == 'cronit:start', ec2_instance['Tags'])),
			map(lambda tag: tag['Value'], filter(lambda tag: tag['Key'] == 'cronit:stop', ec2_instance['Tags']))
		)
		logger.info('%s: %s' % (i, ec2_tuple))
		for i, cron_expression in enumerate(ec2_tuple[1]):
			event_rule_name, event_rule = put_event_rule('start', ec2_tuple[0], cron_expression, i)
			put_event_target(event_rule_name=event_rule_name, id=name, arn=arn)
		for i, cron_expression in enumerate(ec2_tuple[2]):
			event_rule_name, event_rule = put_event_rule('stop', ec2_tuple[0], cron_expression, i)
			put_event_target(event_rule_name=event_rule_name, id=name, arn=arn)
	# TODO: remove old schedules / unused

if __name__ == "__main__":
	cli()