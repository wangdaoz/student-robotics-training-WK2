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

  ## AI Exploration: Package Review 
          After my package was reviewed by Claude Code, it reminds me that: 
              "One real (small) behavioral gap for your troubleshooting section:
               topic_name is only reconfigurable at launch time, not at runtime — if someone tries ros2 param set /status_publisher topic_name new_name while it's running, the parameter callback silently reports success but the publisher keeps using the original topic (only publish_rate has runtime-reconfigure logic). Not a bug relative to what the milestone requires, but it's the kind of "real error encountered" that belongs in your troubleshooting doc so the next intern doesn't waste time confused by it."

          Then, I continued asking: "how to modify current python files to revise it?"
          There are two solutions to solve this problem.

          ● Solution A: Make the rejection honest
            
            1. In "status_publisher_stretch.py", in the section: "def parameter_callback(self, params):..."

             in block: {for param in params: ...}
               
                add "elif" branch:
                   { 
                    elif param.name == 'topic_name':
                        return SetParametersResult(
                                           successful=False,
                                           reason='topic_name can only be set at launch time, not changed at runtime.'
                        ) 
                   }

            2. "status_subscriber.py" 
                At the top of the file, add: <from rcl_interfaces.msg import SetParametersResult>

                In "class StatusSubscriber(Node)" section, 
                   1. in subsection: "def __init__(self)", between the codes:
                     <self.subscription = self.create_subscription(String, topic_name, self.listener_callback, 10)> and
                     <self.get_logger().info('Status Subscriber Node has started.')> add following codes:
                       <self.add_on_set_parameters_callback(self.parameter_callback)>

                   2. Add a new method: "parameter_callback(self, params)"
                             
                              {
                                   def parameter_callback(self, params):   # new method
                                       for param in params:
                                           if param.name == 'topic_name':
                                               return SetParametersResult(
                                                   successful=False,
                                                   reason='topic_name can only be set at launch time, not changed at runtime.'
                                               )
                                       return SetParametersResult(successful=True)
                                  
                              }
                        Result: <Now >ros2 param set /status_publisher topic_name x> will explicitly fail with a clear reason, instead of quietly doing nothing
                 
              ● Solution B: Actually support live topic renaming
                  1. In "status_publisher_stretch.py"

                             in the section: "def parameter_callback(self, params):...", in block: {for param in params: ...}:
                             modify codes in "elif" branch:
                                                {
                                                    elif param.name == 'topic_name':
                                                        if not param.value:
                                                            return SetParametersResult(successful=False, reason='topic_name must not be empty')
                                                        self.destroy_publisher(self.publisher_)
                                                        self.publisher_ = self.create_publisher(String, param.value, 10)
                                                        self.get_logger().info(f'topic_name changed to "{param.value}".')
                                                }

                   2. "status_subscriber.py" 
                        At the top of the file, add: <from rcl_interfaces.msg import SetParametersResult>

                             In "class StatusSubscriber(Node)" section, 
                                1. in subsection: "def __init__(self)", between the codes:
                                   <self.subscription = self.create_subscription(String, topic_name, self.listener_callback, 10)> and  <self.get_logger().info('Status Subscriber Node has started.')> add following codes:
                                   <self.add_on_set_parameters_callback(self.parameter_callback)>

                                2. Add a new method: "parameter_callback(self, params)"

                                {
                                   def parameter_callback(self, params):   # new method
                                       for param in params:
                                           if not param.value:
                                               return SetParametersResult(successful=False, reason='topic_name must not be empty')
                                           self.destroy_subscription(self.subscription)
                                           self.subscription = self.create_subscription(String, param.value, self.listener_callback, 10)
                                           self.get_logger().info(f'topic_name changed to "{param.value}".')
                                       return SetParametersResult(successful=True)
                                  
                                }

                           Note: The catch: publisher and subscriber are two separate nodes, so if you ros2 param set them one at a time, there's a brief window (or a permanent state, if you forget the second one) where they're pointed at different topics and stop talking to each other — the same "mismatched topic names" failure mode called out in Milestone 2.4's common mistakes. That's not a bug in the code, just an inherent property of changing shared config independently per-node, but it's worth a troubleshooting note either way.
 
  ## Reconstruction of Verify Script
          With the help of Claude Code and based on the issues in review feedback, I reconstructed the verify script.
          Many relevant commands in the script were not understanable for me.

          Issue #1: <if [ -n "$LAUNCH_PID" ] && kill -0 "$LAUNCH_PID" 2>/dev/null; then ...>
                  ● '-n'
                    '-n' is a string test operator
                    It asks:
                              "Is the length of this string greater than zero?"
                    It returns:
                                ● true (exit status 0) if the string is not empty

                                ● false (exit status 1) if the string is empty
                     another operator '-z': "is string empty?"
                  
                  ● <kill -0 "$LAUNCH_PID">
                     
                    - 'kill' 
                     send a signal to the process

                    - '-0'
                       A special signal number
                       After it is sent to the process, Linux performs only the checks:
                                       
                                          1. Does this PID exist
                                          2. Does current user have permission to send signal to it

                                        If both conditions are true, return success.

           Issue #2: <<pkill -f "status_publisher_stretch" 2>/dev/null>>
                    I didn't understand what "-f" implicates/means
                      
                     '-f' means: search the entire command line

                     Note 'pkill" stands for process fill; It search preocess by name or pattern

           Issue #3: <trap cleanup EXIT INT TERM>
                   I didn't understand this command.

                   This command tells the shell: "Whenever this script is about to exit normally, or receives an interrupt (Ctrl+C) or a termination request, run the function named cleanup first."

                   - 'trap'
                     trap is a Bash built-in command.
                     Its purpose is to catch signals or shell events and execute some code before the script exits or reacts to that signal.

                      general syntax of trap is:
                        trap COMMAND/FUNC_NAME SIGNAL1, SIGNAL2, ...
           Issue #4: <check "workspace builds from a clean source tree" $?>
                     I didn't understand what '$?' implicates

                     "$?" is an important Bash special variable. It contains:
                                                             the exit status of the command that ran immediately before this line.

           Issue #5: <shift 3>
                    I didn't understand what this command implicates

                    This command means: "Discard the first three positional parameters ($1, $2, and $3) and move all remaining arguments forward."

                    - 'shift' 
                      'shift' means remove given amount of parameters

                      other relevant command: 
                              
                              - '$#' decreases by the number shifted(if the shift succeeds)

                              - '$@' Contains only the remaining arguments after the shift.

           Issue  #6: <LAUNCH_PID=$!>
                       - '$!'
                         '$!' is a special bash variable that contains the Process ID (PID) of the last command that was started  in the background.

           Issue  #7: <ros2 node list | grep -q "/status_subscriber">
                     I didn't understand what '-q' implicates.

                     '-q' option stands for silent mode.
                     with it, without it, grep print machine lines and sets exit status; 
                     With '-q' not output at all, only sets exit status

                     Exit Status for grep: 0(match found), 1(match not found), 2(error occurred)

           Issue  #8: <echo "$hz_output" | grep "average rate" | tail -1 | awk '{print $3}'>
                     in this pipeline command, I didn't understand <tail -1> and <awk '{print $3}'>

                     - <tail -1>
                       
                        - tail
                           print the end(tail) of a file or input

                        - '-1'
                            the last line

                    - <awk '{print $3}'>
                      
                        - awk
                          awk is a text processing language
                          It is designed to:
                                                     ● split text into columns (called fields)
                                                     ● search
                                                     ● calculate
                                                     ● reformat text
                                                     ● generate reports

                        By default, awk uses whitespace(spaces or tabs) as separators.

                        - $3
                           means the third field of the text

           Issue #9: <awk -v m="$measured" -v e="$expected_rate" \
            'BEGIN { d = m - e; if (d < 0) d = -d; exit !(d < e * 0.2) }'>

                  I didn't undertsand '-v' option and the section '\'BEGIN {...}'

                  - '-v'
                    '-v' means: 
                                Create an AWK variable before the AWK program starts.

                        Bash variables only exist in Bash shell; AWK variable only exists inside AWK
                  
                        