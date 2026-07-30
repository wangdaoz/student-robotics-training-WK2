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
           
           issue #1 When I read the script file: "verify_demo.sh", at the begining, I did not understand the first command <set -e>
                
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
                        
           issue #2 <ros2 launch student_robotics status_demo.launch.py &> 
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

           issue #3  When I first ran the file "verify_demo.sh" to test publisher and subscriber nodes, the error from feedback is:
                     "./tests/verify_demo.sh: line 6: install/setup.bash: No such file or directory"

                The currect directory is "student-robotics-training-WK2" but the "install" is a subdiretcory in the parent directory: "robot_ws", so I revised commands in line 6 in to "./robot_ws/install/setup.bash".

                Then, I tried it again and the script succeeded in running.

             