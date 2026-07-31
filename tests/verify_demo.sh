#!/bin/bash
# verify_demo.sh — checks that publisher/subscriber launch and communicate correctly
set -e

source /opt/ros/jazzy/setup.bash
source ./robot_ws/install/setup.bash

echo "Launching demo in background..."
ros2 launch student_robotics status_demo.launch.py &
LAUNCH_PID=$!

#sleep 5  give nodes time to start
# change 'sleep 5' to a loop that checks for the parameter service to be ready
echo "Waiting for parameter service to be ready..."
for i in $(seq 1 30); do
    if ros2 param get /status_publisher publish_rate >/dev/null 2>&1; then
        echo "Parameter service ready after ${i}s"
        break
    fi
    sleep 1
done

echo "Checking nodes are running..."
ros2 node list | grep -q "/status_publisher" && echo "PASS: publisher node found" || echo "FAIL: publisher node missing"
ros2 node list | grep -q "/status_subscriber" && echo "PASS: subscriber node found" || echo "FAIL: subscriber node missing"

echo "Checking publish_rate parameter exists..."
ros2 param get /status_publisher publish_rate && echo "PASS: publish_rate parameter found" || echo "FAIL: publish_rate not a parameter"

echo "Checking topic exists..."
ros2 topic list | grep -q "/robot_status" && echo "PASS: topic found" || echo "FAIL: topic missing"

echo "Checking publish rate..."
timeout 15 ros2 topic hz /robot_status || echo "FAIL: no messages detected"

echo "Shutting down..."
#kill $LAUNCH_PID    only the parent launch process may stop; The child nodes might continue running.
kill -- -$(ps -o pgid= $LAUNCH_PID | tr -d ' ')