#!/bin/bash
export EINK_HOME='/home/pi/eink7in5'
export ENV_DIR='/home/pi/eink7in5/env/bin'
cd $EINK_HOME
nohup $ENV_DIR/python3 $EINK_HOME/weather-indoor.py > $EINK_HOME/logs/start.out 2>&1 &
