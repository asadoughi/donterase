#!/bin/bash

set -e
PROJECT_BASE=/home/amir/dont-erase
LOG_DIR=$PROJECT_BASE/logs
LOG=$LOG_DIR/main.log

NUM_WORKERS=3
USER=amir
GROUP=amir

cd $PROJECT_BASE/main
source $PROJECT_BASE/bin/activate
test -d $LOG_DIR || mkdir -p $LOG_DIR

exec $PROJECT_BASE/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOG 2>>$LOG

