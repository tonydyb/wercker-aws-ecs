# coding: utf-8
from __future__ import unicode_literals
import logging
import sys
import argparse

from ecs import ECSService

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
logging.getLogger("botocore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
h1 = lambda x: logger.info("\033[1m\033[4m\033[94m%s\033[0m\n" % x)
success = lambda x: logger.info("\033[92m✔ %s\033[0m\n" % x)
error = lambda x: logger.info("\033[91m✖ %s\033[0m\n" % x)

# Arguments parsing
parser = argparse.ArgumentParser(description='Deploy Service on ECS')
parser.add_argument('--key', dest='key', required=True)
parser.add_argument('--secret', dest='secret', required=True)
parser.add_argument('--region', dest='region', default='us-east-1')
parser.add_argument('--cluster-name', dest='cluster_name', required=True)
parser.add_argument('--task-definition-name', dest='task_definition_name', required=True)
parser.add_argument('--task-definition-file', dest='task_definition_file', required=True)
parser.add_argument('--task-definition-volumes-file', dest='task_definition_volumes_file', required=False)
parser.add_argument('--service-name', dest='service_name', required=False)
args = parser.parse_args()

try:

    serviceMode = args.service_name is not None

    # Step: Configuring AWS
    h1("Step: Configuring AWS")
    ecs = ECSService(access_key=args.key, secret_key=args.secret, region=args.region)
    success("Configuring AWS succeeded")

    # Step: Check ECS cluster
    h1("Step: Check ECS cluster")
    ecs.describe_cluster(cluster=args.cluster_name)
    success("Checking cluster '%s' succeeded" % args.cluster_name)

    # Step: Register New Task Definition
    h1("Step: Register New Task Definition")
    response = ecs.register_task_definition(family=args.task_definition_name, file=args.task_definition_file, volumes=args.task_definition_volumes_file)
    task_definition_arn = response.get('taskDefinition').get('taskDefinitionArn')
    success("Registering task definition '%s' succeeded" % task_definition_arn)

    if serviceMode:
        # Step: Check ECS Service
        h1("Step: Check ECS Service")
        response = ecs.describe_service(cluster=args.cluster_name, service=args.service_name)
        original_running_count = (response.get('services')[0]).get('runningCount')
        success("Checking service '%s' succeeded (%d tasks running)" % (args.service_name, original_running_count))

        # Step: Update ECS Service
        h1("Step: Update ECS Service")
        response = ecs.update_service(cluster=args.cluster_name, service=args.service_name, taskDefinition=task_definition_arn)
        running_count = (response.get('services')[0]).get('runningCount')
        success("Updating service '%s' with task definition '%s' succeeded" % (args.service_name, task_definition_arn))

    else:
        # Step: run task
        h1("Step: Run task")
        response = ecs.run_task(cluster=args.cluster_name, family=args.task_definition_name)
        success("Task %s succeeded" % (response.get('tasks')[0].get('taskArn')))

except Exception as e:
    error(e)
    sys.exit(1)
