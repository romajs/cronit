#!/usr/bin/env bash

DIR=$(dirname $0)

pip install -r $DIR/requirements-lambda.txt -t $DIR/lib
zip -ru $DIR/dist/cronit-lambda.zip $DIR/cronit-lambda.py $DIR/lib
