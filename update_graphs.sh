#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -e
. $DIR/bin/activate
python $DIR/bluelytics/manage.py export_graph bluelytics/data/graphs/evolution.json
python $DIR/bluelytics/manage.py export_currencies bluelytics/data/json/currency.json
