cronit
======

## Usage

```
Usage: cronit [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level TEXT  Set logging level
  --help            Show this message and exit.

Commands:
  sync  Update all cronit schedules
```

## Execution

Can be executed as `./cronit.py`

To use with bash completion, is needed to run the following:

```
source ./.virtualenv/bin/activate
source ./bash-complete.sh
```

Then execute as `cronit` only

## Install

`./install.sh`

## Requirements

* Python 2.7+
* Python PIP
* Python Virtualenv
