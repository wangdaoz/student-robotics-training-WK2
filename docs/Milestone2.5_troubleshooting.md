### Engineering Tasks
  
  ## task1. Add one launch command that starts publisher and subscriber together.

         Issue 1: after inputting commands: <colcon build --packages-select student_robotics>, <source install/setup.bash> in a   build-in terminal or in a new terminal <source /opt/ros/jazzy/setup.bash>, <source ~/student-robotics-training-WK2>,
         Next input command: 
                            <ros2 launch student_robotics status_demo.launch.py>
             the error from the terminal is:
              "file 'status_demo.launch.py' was not found in the share directory of package 'student_robotics' which is at '/home/kevin-lianhu/student-robotics-training-WK2/robot_ws/install/student_robotics/share/student_robotics'"
        
            This error means that ROS 2 can not look for file "file 'status_demo.launch.py" in the share directory of package 'student_robotics'. 
              
              To solve it, 
            1. open the file: 'setup.py' via the path: '/home/kevin-lianhu/student-robotics-training-WK2/robot_ws/src/student_robotics/setup.py'.
            2. add following codes:
                  
                  At the bottom, add: <import os>, <from glob import glob>, <from setuptools import setup>

                  In "setup(...), in "data_files=[(...),(...),(...)], add a segment of codes:
                                                <(os.path.join('share', package_name, 'launch'),
                                                                      glob('launch/*.launch.py')),>

                    -- os.path.join('share', package_name, 'launch')
                        os.path.join(xxx,xxx,xxx) constructs a filesystem path that works correctly on different operating systems. In addition, the 'package_name' is given on the "setup.py" when create the package.

                    -- glob('launch/*.launch.py')
                        search for files matching a specific pattern.
                        search files inside the 'launch/' directory whose name end with '.launch.py'.

                    -- puting together
                        "Install all the .launch.py files from my local launch/ directory into the package's share/<package_name>/launch/ directory."
                              
                    Note: don't ignore the comma ',' at the end
           
         Issue 2: 
              after inputting the same command as mentioned above: the feedback error is:
                       ["[ERROR] [launch]: Caught exception in launch (see debug for traceback): Caught multiple exceptions when  trying to load file of format [py]:
                         - SyntaxError: invalid syntax. Perhaps you forgot a comma? (status_demo.launch.py, line 6)
                         - InvalidFrontendLaunchFileError: The launch file may have a syntax error, or its format is unknown"]
                To solve it:
                 Add the comma at the end of the added segment of codes in "data_files[...] section.

  ## task 5. Add a verification script
           
           Issue #1 When I read the script file: "verify_demo.sh", at the begining, I did not understand the first command <set -e>
                
                Then I asked this question to my AI tool: chatgpt, then I got the solution:
                    <set -e> tells the shell: "If any command exits with a non-zero status (an error), stop executing the script immediately."
                   
                     -- set
                        configurable or change the settings of the shell

                     -- '-'
                        enables an option

                        '+'
                         disables an option

                     -- 'e'
                        Exit immediately if a command fails
                         other options:
                         'u': Treat undefined variables as errors.

                         'x': Print each command before running it

                         '-o pipefail': make a pipeline fail if any command in the pipeline fails, not just the last one
                     -- exit status
                         
                         ● 0 means success

                         ● Any non-zero value means failure
                        
           Issue #2 <ros2 launch student_robotics status_demo.launch.py &> 
                    <LAUNCH_PID=$!>  
                    in the script file: "verify_demo.sh"
                  -- ros2 
                    ros2 is command line interface (CLI)

                  -- '&'
                    This is pure bash syntax -- it is not a part of ROS 2
                    It means: run the preceding command in the background
                 
                  -- 'LAUNCH_PID'
                      A shell variable

                  -- '$!'
                      A special bash variable,
                       it means: 
                                 the Process ID (PID) of the most recently started background process.

           Issue #3  When I first ran the file "verify_demo.sh" to test publisher and subscriber nodes, the error from feedback is:
                     "./tests/verify_demo.sh: line 6: install/setup.bash: No such file or directory"

                The currect directory is "student-robotics-training-WK2" but the "install" is a subdiretcory in the parent directory: "robot_ws", so I revised commands in line 6 in to "./robot_ws/install/setup.bash".
                Then, I tried it again and the script succeeded in running.

           Issue #4 In engineering task 8: Perform a clean-clone release test. After I ran the finished launch file: "status_demo.launch.py", in a a new terminal, after I inputted relevant comands to source the terminal. Then, I inputted the test commands <ros2 node list>, <ros2 topic list>, <ros2 topic hz /robot_status> respectively.
              
            The errors are: 
                             the result of the nodes present is: 
                                                                    "status_publisher
                                                                     status_publisher
                                                                     status_subscriber
                                                                     status_subscriber"

                             the result of average publish rate is 2.000 or other values but the default publish rate is 1.0.

             Solution to this problem:
                       Step 1: check how many publish processes are in progress
                            input command: <ps aux | grep status_publisher> or <ros2 node list>

                            -- 'ps'
                                 'ps' stands for Process Status;
                                 It is a Linux command used to display information about the processes currently running on the system.

                            -- aux
                               it is equivalent to a u x

                               - 'a'
                                   Show processes belonging to all users that have a terminal (TTY).
                                   Without a, ps normally shows only your current shell's processes.

                               - 'u'
                                   Display processes in a user-oriented format.

                                   Instead of showing only process IDs, it includes useful columns like:
                                     ● owner

                                     ● CPU usage

                                     ● memory usage

                                     ● start time

                                     ● command

                                - 'x'
                                   Show processes without a controlling terminal. Many background services don't have a terminal.
                             
                                 if there are two or more status publisher processes, then do step 2

                          Step 2 Fix it properly (doesn't recur)
                                 The real bug is in verify_demo.sh's cleanup step. Kill the whole process group instead of just the launch PID.

                                 Open the test script file: "verify_demo.sh",
                                 change the last line: <kill LAUNCH_PID> → <kill -- -$(ps -o pgid= $LAUNCH_PID | tr -d ' ')>
                
                                 <kill -- -$(ps -o pgid= $LAUNCH_PID | tr -d ' ')>

                                  -- kill 
                                     'kill' sends a signal to one or more process

                                  -- ps -o pgid= $LAUNCH_PID
                                     '-o' output only the specified columns

                                     'pgid' Process Group ID
                                      each process has a different process id.

                                  -- <tr -d ' '>
                                      
                                      'tr' translate characters

                                      '-d' means delete characters; here delete all spaces.


                                  here translate characters(PGID) returned by previous commands and remove all spaces

                          Step 3: run the script: verify_demo_sh again.

           Issue #5
               After I ran "verify_demo.sh", the running results were:                                                                                                        {Launching demo in background...
               [INFO] [launch]: All log files can be found below /home/kevin-lianhu/.ros/log/2026-07-30-13-28-42-841418-CAGEWANG-15636
               [INFO] [launch]: Default logging verbosity is set to INFO
               [INFO] [status_publisher_stretch-1]: process started with pid [15648]
               [INFO] [status_subscriber-2]: process started with pid [15649]
               [status_publisher_stretch-1] [INFO] [1785443366.198127077] [status_publisher]: Status publisher started at 1.0 Hz.
               [status_subscriber-2] [INFO] [1785443325.774953751] [status_subscriber]: Status Subscriber Node has started.
               Checking nodes are running...
               PASS: publisher node found
               PASS: subscriber node found
               Checking publish_rate parameter exists...
               Wait for service timed out waiting for parameter services for node /status_publisher
               FAIL: publish_rate not a parameter
               Checking topic exists...
               PASS: topic found
               Checking publish rate...
               WARNING: topic [/robot_status] does not appear to be published yet
               FAIL: no messages detected
               Shutting down...
               Terminated }

            Analysis:
                 Look at the two "started" messages closely:
                    {
                        [status_publisher_stretch-1] [INFO] [1785443366.198127077] [status_publisher]: Status publisher started at 1.0 Hz.
                        [status_subscriber-2] [INFO] [1785443325.774953751] [status_subscriber]: Status Subscriber Node has started.
                    }

                 Those numbers are Unix epoch timestamps. Subtracting them: 1785443366.198 − 1785443325.775 ≈ 40.4 seconds. Even though both nodes were launched together in the same command, one of them took ~40 seconds longer than the other to fully initialize and report ready. Your original script only waits 5 seconds total before running any checks — nowhere close to enough on this particular machine/run.

                   ● <ros2 node list> (used for your PASS checks) only needs lightweight graph info — which node names exist —   and that propagates fast.

                   ● <ros2 param get> needs the node's parameter service to be fully registered and matched over DDS — a heavier, slower step. Hence: "Wait for service timed out waiting for parameter services for node /status_publisher."

                   ● <ros2 topic hz> needs a publisher-subscriber match to form over DDS before any message can arrive — also slower than basic node discovery. Hence: "topic does not appear to be published yet" → no messages within your timeout 5 window → FAIL.
                
                Both are downstream of the same discovery delay; they just failed for slightly different sub-reasons (service match vs. topic match) within roughly the same time budget.

        Solution:
                  1. A fixed <sleep 5> is a race condition by nature — it works until it doesn't, exactly what just happened. Better to actively wait for readiness instead of guessing a duration:

                   {
                                  echo "Waiting for parameter service to be ready..."
                                  for i in $(seq 1 30); do
                                      if ros2 param get /status_publisher publish_rate >/dev/null 2>&1; then
                                          echo "Parameter service ready after ${i}s"
                                          break
                                      fi
                                      sleep 1
                                  done
                   }
                        -- <ros2 param get /status_publisher publish_rate>
                            retrieve the value of the parameter: publish-rate in the node '/status_publisher'
                            If it succeeds, exit with code: 0
                            Otherwise, exit with code: 1

                        -- <>/dev/null>
                             if previous command succeeds, send the stand output(stdout) into "/dev/null"

                           ● /dev/null
                             /dev/null is a special file in Linux that simply throws away anything written to it.
                             So nothing is displayed in terminal

                        -- < 2>&1 >
                            Linux programs have three standard streams:
                                 Number          Name          Purpose
                                 0               stdin         input
                                 ------------------------------------------
                                 1               stdout        normal output
                                 ------------------------------------------
                                 2               stderr        error messages
                                 -------------------------------------------

                           If the previous command return an error message in stderr stream:
                                 2>&1: redirect stderr(2) to wherever stdout(1) is currently going

                                 Since stdout already goes to /dev/null, both streams go there.


                   2. lengthen the timeout 5 on the ros2 topic hz check to timeout 15 too.

               after modifying the test script, run the script again. Observe the results.