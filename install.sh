#!/usr/bin/env bash

DIR=$(dirname $0)

if [[ ! -d $DIR/.virtualenv ]]; then
	virtualenv $DIR/.virtualenv
fi

source $DIR/.virtualenv/bin/activate
pip install -r $DIR/requirements.txt

pip install --editable $DIR
$DIR/bash-complete.sh

echo "
In your current shell:

To use \"cronit\", run the following:
source $DIR/.virtualenv/bin/activate

When you done, run:
deactivate

To enable bash completion, run:
source $DIR/bash-complete.sh
"
