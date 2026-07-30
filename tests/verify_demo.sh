#!/bin/bash
# verify_demo.sh — checks that publisher/subscriber launch and communicate correctly
set -e

source /opt/ros/jazzy/setup.bash
source ./robot_ws/install/setup.bash

echo "Launching demo in background..."
ros2 launch student_robotics status_demo.launch.py &
LAUNCH_PID=$!

sleep 5   # give nodes time to start

echo "Checking nodes are running..."
ros2 node list | grep -q "/status_publisher" && echo "PASS: publisher node found" || echo "FAIL: publisher node missing"
ros2 node list | grep -q "/status_subscriber" && echo "PASS: subscriber node found" || echo "FAIL: subscriber node missing"

echo "Checking publish_rate parameter exists..."
ros2 param get /status_publisher publish_rate && echo "PASS: publish_rate parameter found" || echo "FAIL: publish_rate not a parameter"

echo "Checking topic exists..."
ros2 topic list | grep -q "/robot_status" && echo "PASS: topic found" || echo "FAIL: topic missing"

echo "Checking publish rate..."
timeout 5 ros2 topic hz /robot_status || echo "FAIL: no messages detected"

echo "Shutting down..."
kill $LAUNCH_PID