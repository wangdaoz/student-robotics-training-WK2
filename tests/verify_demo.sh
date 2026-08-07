#!/bin/bash
# verify_demo.sh — proves, from a clean build, that the student_robotics
# publisher/subscriber demo launches with one command, communicates
# correctly, and honors its configurable parameters (publish_rate,
# topic_name), as required by Milestone 2.5.
#
# Run from anywhere:
#   ./tests/verify_demo.sh
 
set -u # unset variables are errors. NOT using `set -e`: several checks
         # below are expected to "fail" mid-script (e.g. a param not yet
         # ready, or `timeout` killing a long-running command) without
         # aborting the whole run. Pass/fail is tracked explicitly and the
         # script's own exit code is set at the very end (fix #2).

# ---------------------------------------------------------------------------
# Fix #4: resolve every path relative to this script's own location, not the
# caller's current directory, so it works no matter where it's invoked from.
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WS_DIR="$REPO_ROOT/robot_ws"
 
FAIL_COUNT=0
LAUNCH_PID=""

# ---------------------------------------------------------------------------
# Fix #2: every check goes through here so a FAIL is counted, not just
# printed. The script's final exit code reflects FAIL_COUNT.
# ---------------------------------------------------------------------------
check() {
    local description="$1"
    local result="$2"   # 0 = pass, nonzero = fail
    if [ "$result" -eq 0 ]; then
        echo "PASS: $description"
    else
        echo "FAIL: $description"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# ---------------------------------------------------------------------------
# Fix #6: cleanup is a trap, not a script-ending line, so it runs no matter
# how the script exits (normal end, early return, Ctrl-C, or an error).
# It kills the whole process group (publisher + subscriber), with a
# fallback by process name in case process-group lookup fails.
# ---------------------------------------------------------------------------
cleanup() {
    if [ -n "$LAUNCH_PID" ] && kill -0 "$LAUNCH_PID" 2>/dev/null; then
        local pgid
        pgid=$(ps -o pgid= "$LAUNCH_PID" 2>/dev/null | tr -d ' ')
        if [ -n "$pgid" ]; then
            kill -- "-$pgid" 2>/dev/null
        else
            kill "$LAUNCH_PID" 2>/dev/null
        fi
    fi
    # Belt-and-suspenders: catch any orphaned node the pgid kill missed.
    pkill -f "status_publisher_stretch" 2>/dev/null
    pkill -f "status_subscriber" 2>/dev/null
    LAUNCH_PID=""
}
trap cleanup EXIT INT TERM
set +u
source /opt/ros/jazzy/setup.bash
set -u

# ---------------------------------------------------------------------------
# Fix #5: prove clean-clone reproducibility by removing any existing build
# output and building from source every time this script runs, instead of
# assuming install/ already exists.
# ---------------------------------------------------------------------------
echo "Removing existing build artifacts to force a clean build..."
rm -rf "$WS_DIR/build" "$WS_DIR/install" "$WS_DIR/log"
 
echo "Building workspace from source..."
( cd "$WS_DIR" && colcon build --packages-select student_robotics )
check "workspace builds from a clean source tree" $?
 
if [ "$FAIL_COUNT" -gt 0 ]; then
    echo "Build failed — skipping runtime checks."
    exit 1
fi

set +u 
source "$WS_DIR/install/setup.bash"
set -u

# ---------------------------------------------------------------------------
# Launches the demo with the given launch arguments, waits for readiness,
# and checks that the expected topic exists and publishes at roughly the
# expected rate. Used once with defaults and once with overrides, which
# covers fix #7 (actually testing the configurable behavior, not just the
# default path).
# ---------------------------------------------------------------------------
run_demo_check() {
    local label="$1"
    local expected_topic="$2"
    local expected_rate="$3"
    shift 3
    local launch_args=("$@")
 
    echo ""
    echo "=== $label ==="
    echo "ros2 launch student_robotics status_demo.launch.py ${launch_args[*]}"
    ros2 launch student_robotics status_demo.launch.py "${launch_args[@]}" &
    LAUNCH_PID=$!
 
    # Fix #1: readiness loop now FAILS explicitly if it never becomes ready,
    # instead of silently continuing into checks that would fail for the
    # wrong reason.
    local ready=false
    for i in $(seq 1 30); do
        if ros2 param get /status_publisher publish_rate >/dev/null 2>&1; then
            echo "Parameter service ready after ${i}s"
            ready=true
            break
        fi
        sleep 1
    done
    if [ "$ready" != true ]; then
        check "$label: parameter service became ready within 30s" 1
        cleanup
        return
    fi
 
    ros2 node list | grep -q "/status_publisher"
    check "$label: publisher node found" $?
 
    ros2 node list | grep -q "/status_subscriber"
    check "$label: subscriber node found" $?
 
    ros2 topic list | grep -q "/${expected_topic}$"
    check "$label: topic /${expected_topic} exists" $?
 
    local rate_reported
    rate_reported=$(ros2 param get /status_publisher publish_rate 2>/dev/null)
    echo "$rate_reported" | grep -q "$expected_rate"
    check "$label: publish_rate parameter reports ${expected_rate}" $?
 
    # Fix #3: `timeout` killing `ros2 topic hz` after N seconds is the
    # *expected* way this command ends — it runs until stopped. Its exit
    # code (124 on timeout) is not a failure signal on its own. Parse the
    # captured output instead of trusting the exit code.
    local hz_output
    hz_output=$(timeout 15 ros2 topic hz "/${expected_topic}" 2>&1)
    if echo "$hz_output" | grep -q "average rate"; then
        local measured
        measured=$(echo "$hz_output" | grep "average rate" | tail -1 | awk '{print $3}')
        echo "measured rate: ${measured} Hz (expected ~${expected_rate} Hz)"
        awk -v m="$measured" -v e="$expected_rate" \
            'BEGIN { d = m - e; if (d < 0) d = -d; exit !(d < e * 0.2) }'
        check "$label: measured rate is close to expected ${expected_rate} Hz" $?
    else
        check "$label: messages detected on /${expected_topic}" 1
    fi
 
    cleanup
    sleep 1   # let the topic/ports fully release before the next launch
}
 
run_demo_check "Default configuration" "robot_status" "1.0"
 
run_demo_check "Configured override" "robot_status_test" "2.0" \
    "publish_rate:=2.0" "topic_name:=robot_status_test"
 
echo ""
echo "=================================="
if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "ALL CHECKS PASSED"
    exit 0
else
    echo "$FAIL_COUNT CHECK(S) FAILED"
    exit 1
fi