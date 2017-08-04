#!/usr/bin/env python
import boto3, datetime, lib.croniter as croniter

def handler(event, context):

	ec2_client = boto3.client('ec2')
	
	ec2_instances = ec2_client.describe_instances(Filters=[
		{'Name': 'tag-key', 'Values': ['cronit:start']},
		{'Name': 'tag-key', 'Values': ['cronit:stop']}
	])

	items=[]

	for reservation in ec2_instances['Reservations']:
		for ec2_instance in reservation['Instances']:
			item = (
				ec2_instance['InstanceId'],
				map(lambda tag: tag['Value'], filter(lambda tag: tag['Key'] == 'cronit:start', ec2_instance['Tags'])),
				map(lambda tag: tag['Value'], filter(lambda tag: tag['Key'] == 'cronit:stop', ec2_instance['Tags']))
			)
			items.append(item)

	instances_to_start=[]
	instances_to_stop=[]

	now = datetime.datetime.now().replace(second=0, microsecond=0)
	print 'Date now: %s' % now

	delayed = now - datetime.timedelta(minutes=1)
	print 'Date delayed: %s' % delayed

	for item in items:

		print 'Parsing item: ', item

		print 'Parsing start cron`s:'
		for i, cron_start in enumerate(item[1]):
			next_cron = croniter.croniter(cron_start.replace('?', '*'), delayed).get_next(datetime.datetime)
			print 'Instance %s next_cron: %s' % (item[0], next_cron)
			if next_cron <= now:
				instances_to_start.append(item[0])

		print 'Parsing stop cron`s:'
		for i, cron_stop in enumerate(item[2]):
			next_cron = croniter.croniter(cron_stop.replace('?', '*'), delayed).get_next(datetime.datetime)
			print 'Instance %s next_cron: %s' % (item[0], next_cron)
			if next_cron <= now:
				instances_to_stop.append(item[0])

	print 'Starting instances: %s' % instances_to_start
	instances_to_start and ec2_client.start_instances(InstanceIds=instances_to_start)

	print 'Stopping instances: %s' % instances_to_stop
	instances_to_stop and ec2_client.stop_instances(InstanceIds=instances_to_stop)

	print 'Done.'

if __name__ == "__main__":
		handler({}, {})
