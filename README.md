Wercker step for AWS ECS
=======================

This wercker step allows to deploy Docker containers with [AWS ECS](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_GetStarted.html) service or run a task outside of a service.

Please read the [AWS ECS](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html) documentation and [API](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/Welcome.html) before using this step.

The step is written in Python 2.7 and use Pip and Boto3 module.


## AWS ECS workflow

To deploy an application with AWS ECS, the Wercker step follow this steps:

There is two different flows depending if the Wercker step is running in "service mode" or in "task only mode".
If `service-name` is provided in the configuration, the service mode is used.

#### Step [Configuring AWS](http://docs.aws.amazon.com/cli/latest/reference/configure/index.html)

This initial step consists on configuring AWS.

The following configuration allows to setup this step :

* `key` (required): AWS Access Key ID
* `secret` (required): AWS Secret Access Key
* `region` (optional): Default region name

#### Step [Checking ECS Cluster](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeClusters.html)

This step check a previously created ECS cluster exists.

The following configuration allows to setup this step :

* `cluster-name` (required): The name of the cluster to deploy the service

#### Step [Checking ECS Service](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeServices.html) (Skipped in task only mode)

This step check a previously created ECS service exists. The service MUST be created before using this step.

The following configuration allows to setup this step :

* `service-name` (optional): The name of the service to deploy

#### Step [Create New Task Definition ](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RegisterTaskDefinition.html)

This step register a new task definition for the service.

The following configuration allows to setup this step :

* `task-definition-name` (required): The name of the task definition
* `task-definition-file` (required): The file containing the task definition


## In service mode:

#### Step [Update ECS Service](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html)

This step update the service with the new revision.

## In task only mode:

#### Step [Run task](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html)

This step run a task on a single node and wait for its completion. The step fail if the task can't be run or if its command exit code is different from 0.

## Example

The following example deploy an `hello` service on ECS :

```
deploy:
  steps:
    - 1science/aws-ecs:
        key: aws_access_key_id
        secret: aws_access_secret_id
        cluster-name: staging
        task-definition-name: hello-migrate-db
        task-definition-file: /app/hello-migrate-db-task-definition.json
    - 1science/aws-ecs:
        key: aws_access_key_id
        secret: aws_access_secret_id
        cluster-name: staging
        service-name: hello
        task-definition-name: hello
        task-definition-file: /app/hello-task-definition.json
```
