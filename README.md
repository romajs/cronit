cronit
======

## CLI

### Requirements

* Python 2.7+
* Python PIP
* Python Virtualenv

### Install

`./install.sh`

### Authentication

[]()
[See the boto3 guide for credentials](http://boto3.readthedocs.io/en/latest/guide/configuration.html#credentials)

### Permissions

Create the role **CronitCLIRole** with the following:

*This role must be then associated with your current user/credentials*

**CronitCLIPolicy.json**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "events:ListRules",
                "events:PutRule",
                "events:DeleteRule",
                "events:PutTargets",
                "events:RemoveTargets",
                "lambda:AddPermission",
                "lambda:RemovePermission"
            ],
            "Resource": [
                "arn:aws:events:{region}:{accountId}:rule/*",
                "arn:aws:lambda:{region}:{accountId}:function:cronit"
            ]
        }
    ]
}
```

**CronitCLIDescribeInstancesPolicy.json**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
}
```


### Execution

Can be executed both as `./cronit.py` and `cronit`, but then it is needed to run:

```
source ./.virtualenv/bin/activate
source ./bash-complete.sh
```

*Also bash completion is enabled with this*

### Usage

```
Usage: cronit [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level TEXT  Set logging level
  --help            Show this message and exit.

Commands:
  sync  Update all cronit schedules
```

Then execute as `cronit` only

## AWS Lambda

### Permissions

Create the role **CronitLambdaExecutionRole** with the following:

*This role must be then associated with your **cronit** lambda function*

**CronitLambdaExecutionPolicy.json**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```


### Configuration

* TODO
