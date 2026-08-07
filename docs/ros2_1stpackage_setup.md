## Computer
    ● Operating system: WSL

    ● Python version: Python 3.12.3

    ● Git version: 2.43.0

    ● VS Code installed: yes

    ● Claude Code installed: yes

## Steps Completed && Commands Used
  
   Task 1.Create student_robotics inside robot_ws/src using ament_python.
    # Step 1: Make sure you're inside your workspace's 'src' directory
        
         <cd ~/robot_ws/src>
           -cd access to the target directory

    # Step 2: Make sure ROS 2 is sourced
     
         <source /opt/ros/<distro>/setup.bash>

        Replace <distro> with whatever ROS 2 version you installed in Milestone 2.2 (e.g. humble, jazzy, iron). Worth checking with <echo $ROS_DISTRO> to confirm it's already sourced.

    # Step 3: Run the package creation command
         <ros2 pkg create --build-type ament_python student_robotics>

    # Step 4: Inspect every file generated
               This generates a folder structure like:

                   robot_ws/
                       └── src/
                            └── student_robotics/
                                 ├── package.xml
                                 ├── setup.py
                                 ├── setup.cfg
                                 ├── resource/
                                 |        └── student_robotics
                                 ├── student_robotics/
                                 │        └── __init__.py
                                 └── test/   
               open package.xml, setup.py, setup.cfg, the resource/ file, and the test/ directory and read what's in them.
    # Step 5: Confirm the package "student_robotics" is placed inside the directory "robot_ws/src/"
   ___________________________________________________________________________________________________________________________

   Task 2: Build the workspace and source the result
       
      # Step 1: Go to the root of your workspace (not inside the src/)
                   <cd ~/robot_ws>

      # Step 2: Build the workspace:
                   <colcon build> : build the workspace with colcon

                    Expected Results:
                                     Starting >>> student_robotics
                                     Finished <<< student_robotics [x.xx s]

                                     Summary: 1 package finished [x.xx s]
                      Note: If you see errors instead, they're almost always caused by a malformed package.xml or setup.py — worthopening those back up and checking syntax if the build fails.

      # Step 3: Check what the 'build' created
          After a successful build, you'll see new top-level folders appear in robot_ws/:
                                                                      robot_ws/
                                                                      ├── build/
                                                                      ├── install/
                                                                      ├── log/
                                                                      └── src/
                                                            ● install/ — the usable, "installed" version of your package 

                                                            ● build/ — intermediate build artifacts

                                                            ● log/ — build logs, useful for debugging if something goes wrong

      # Step 4: Source the install
                <source install/setup.bash> 
                add newly built package to ROS 2's search path for the current terminal session
                so commands like ros2 pkg list or ros2 run can find student_robotics.

      # Step 5: Verify it's discoverable
                 <ros2 pkg list | grep student_robotics>
  _________________________________________________________________________________________________________________________________

   Task 3 Add a minimal node executable and run it through ros2 run
     # Step 1: navigate to your package's Python module folder
                <cd ~/student-robotics-training-WK2/robot_ws/src/student_robotics/student_robotics>

     # Step 2: Create a minimal node file
                 <nano my_node.py>

     # Step 3: Register it as an executable in setup.py
                 <cd ..>  go to the folder containing "setup.py"
                 <nano setup.py> 

                 find the "entry_points" section
                 Add a line inside 'console_scripts':
                            entry_points={
                                'console_scripts': [
                                    'my_node = student_robotics.my_node:main',
                                ],
                            },

                This tells ROS 2: "the command my_node should call the main() function inside student_robotics/my_node.py." Save and exit.

      # Step 4: rebuild the workspace
                 <cd ~/student-robotics-training-WK2/robot_ws>
                 <colcon build>
                
                Note: 
                     You need to rebuild every time you add/change an executable or entry point — the install layout has to regenerate

      # Step 5: Resource
             <source install/setup.bash>
             Note: 
                  (If you added the sourcing line to ~/.bashrc already, a fresh terminal will also pick this up automatically — but after a rebuild, re-source in your current terminal too, since it won't pick up changes on its own.)

      # Step 6: Running
                 <ros2 run student_robotics my_node>

                 Expected output:
                      [INFO] [my_node]: my_node has started

                Press "Ctrl+C" to stop it

              Note:
                   If <ros2 run> says it can't find the executable, the two most common causes are: forgetting to rebuild after editing setup.py, or forgetting to re-source after rebuilding. Let me know if you hit either error and I can help debug.
  _________________________________________________________________________________________________________________________________

  Task 4: Write docs/ros2_package_structure.md explaining each important generated file
         Step 1: check whether the directory docs is existing in the directory: "student-robotics-training-WK2", if not exist
                    <mkdir -p docs>

         Step 2: create the structure file:
             <touch docs//ros2_package_structure.md> or <nano docs/ros2_package_structure.md>
         Step 3: edit the file with relevant contents

___________________________________________________________________________________________________________________________________
   Task 5: Add correct metadata and dependencies to package.xml and setup.py.
          Step 1: Open 'package.xml'
                <nano ~/student-robotics-training-WK2/robot_ws/src/student_robotics/package.xml>
                It was auto-generated with placeholder values like TODO for description, license, and maintainer.
                What to actually change:

                   <description> — replace the placeholder with a real one-line summary of what the package does.

                   <maintainer email="..."> — put your real name and email. This isn't cosmetic — it's how other engineers know who to contact about the package.

                   <license> — pick a real license (Apache-2.0 is the ROS 2 default convention; check what your repo's overall LICENSE file says and match it).

                   <depend>rclpy</depend> — add this line. Your node imports rclpy, so it must be declared as a dependency. This is what lets rosdep install and other tooling know your package needs rclpy to build/run.
              Note: 
                 If you add more imports later (e.g. std_msgs in Milestone 2.4), you'll add a <depend> line for each one.

          Step 2: Open 'setup.py'
                  <nano ~/student-robotics-training-WK2/robot_ws/src/student_robotics/setup.py>

                  Fill in the matching metadata fields:
                         What to check/change:

                   ● version, maintainer, maintainer_email, description, license — should match package.xml exactly. Mismatches here are a common review flag since both files describe the same package.

                   ● entry_points — you already added this in the previous task; just confirm it's still correct.

                   ● install_requires — this is Python-level dependency declaration (as opposed to ROS-level in package.xml). For a simple rclpy-based node, setuptools is typically all that's needed here since rclpy itself is provided by the ROS 2 install, not pip.

          Step 3: Rebuild and re-source to confirm nothing broke
                 <cd ~/student-robotics-training-WK2/robot_ws>

                 <colcon build>

                 <source install/setup.bash>

                 <ros2 run student_robotics my_node>
                
                If it still runs cleanly, your metadata changes didn't break anything structurally — you've just made the package accurately describe itself.
## Problems Encountered
   Task 2:  Build the workspace and source the result
             To avoid re-source for each terminal, I added the path "~/robot_ws/install/setup.bash" to the "~/.bashrc".
             I inputted <source ~/.bashrc>

             the feedback error: "bash: /home/kevin-lianhu/robot_ws/install/setup.bash: No such file or directory"

             I asked claude code for help. The claude code explained that "install/setup.bash doesn't actually exist at ~/robot_ws/install/setup.bash--so colcon build either hasn't been run successfully yet, or the workspace lives somewhere else." 

             It reminded me possible causes:

                 1. Build hasn't been run in this environment/terminal yet

                    If you don't see build/, install/, and log/ folders, colcon build never completed. Go back to "~/robot_ws" and run <colcon build> again

                 2. The build failed sliently or partially
                    
                    If install/ exists but install/setup.bash specifically is missing, check the build logs:
                     check the build log: <cat ~/robot_ws/log/latest_build/events.log> 

                 3. workspace isn't actually at ~/robot_ws
                     
                    Double check where you actually ran ros2 pkg create and colcon build earlier. 
                    find it by inputting the command: <find ~ -maxdepth 3 -name "student_robotics" 2>/dev/null>
                   This will show you the real path. If it turns out to be somewhere like ~/dev/robot_ws instead, you'll need to fix the path in ~/.bashrc to match.

                 4. Quick sanity check
                     <ls ~/> 
                     what actually in your home directory

             I checked each possible causes and eliminated the first two causes. After I inputted <<find ~ -maxdepth 3 -name "student_robotics" 2>/dev/null>, nothing was shown. Next I inputted <find ~ -name "student_robotics">, many items was displayed in my terminal. Then I discovered the workspace(robot_ws) is in the "~/student-robotics-training-WK2". Then. I inputted <ls ~/>, "student-robotics-training-WK2" is in the home directory in my terminal. So I thought the cause wa: "workspace isn't actually at ~/robot_ws" but still not sure. I told the claude code the path of my workspace: "/home/kevin-lianhu/student-robotics-training-WK2/robot_ws". Then, claude code answered me the actual cause is workspace isn't in "~/robot_ws". 
              
            After figuring out actual cause, The claude told me open the "~/.bashrc", find the line "~/robot_ws/install/setup.bash" at the bottom and replace it with actual path "~/student-robotics-training-WK2/robot_ws/install/setup.bash".
            Then, I saved and exited ".bashrc" file 

            Then, I re-sourced the .bashrc again: <source ~/.bashrc>;
            Verify it: inputted command: <ros2 pkg list | grep student_robotics>, the terminal shown the correct answer: the name of the package: "student_robotics".
    _______________________________________________________________________________________________________________________________

    Task 3: Add a minimal node executable and run it through ros2 run.
             After I inputted <ros2 run student_robotics my_node>
             I saw the expected output from the terminal but after I pressed "Ctrl+C" to stop it. the terminal gave me some error message:
                     in main
                             rclpy.shutdown()
                              File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/__init__.py", line 134, in shutdown
                                                _shutdown(context=context)
                              File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/utilities.py", line 82, in shutdown
                                                context.shutdown()
                              File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/context.py", line 129, in shutdown
                                                self.__context.shutdown()
                              rclpy._rclpy_pybind11.
                              RCLError: failed to shutdown: rcl_shutdown already called on the given context, at ./src/rcl/init.c:333
                              [ros2run]: Process exited with failure 1

            I  didn't understand this message, so I asked claude for helo and it gave me detail explaination about this error message.
                The cause is 
                When I pressed "Ctrl+C", 'rclpy' has its own internal signal handler for SIGINT. In many recent ROS 2 versions, that handler already calls 'rclpy.shutdown()' on your behalf as part of unwinding 'rclpy.spin()'. Then my codes 'finally' block runs and calls 'rclpy.shutdown()' again but the context is already shutdown so I get the RCLerror message:
                         "RCLError: failed to shutdown: rcl_shutdown already called on the given context, at ./src/rcl/init.c:333"
                      
                Next, it told me that before I shut down the ROS 2 client library, I should knwo whether the context is stil active.
                    In the robot_ws/src/student_robotics/student_robotics/my_node.py, in 'finally' block before shuting down library, adding a segment of code:
                                                           <finally:
                                                               node.destroy_node()
                                                               if rclpy.ok():
                                                                     rclpy.shutdown()>

                Then:
                    from "~/student-robotics-training-WK2/robot_ws", rebuild: <colcon build>

                    Resource: <source install/setup.bash>

                    Run again: <ros2 run student_robotics my_node>, then pressed "Ctrl+C" to stop it

                Finally, the error was gone.

    Task 5: Add a minimal node executable and run it through ros2 run.

             In 'package.xml' and 'setup.py', when I modified the item "LICENSE", the claude first advised me to wirite "Apache-2.0" or "MIT". But when I created this repo in GitHub, I didn't set 'LICENSE'. Then I asked claude further, the claude said "In that case, common choices for student/training repos are Apache-2.0 or MIT — either is a reasonable default, but it's a decision for whoever owns the repo, not something to pick silently on your own." So, I didn't modify this item.

    Task 5: Add a minimal node executable and run it through ros2 run.
         In robot_ws/src/student_robotics/student_robotics/my_node.py, my segments of codes I didn't understand.

         Then, with the help of AI tools, I learned the following knowledge:
          
                               """
                                rclpy is the Python client library for ROS 2 (Robot Operating System 2). 
                                 It allows you to write ROS 2 applications (called nodes) in Python.

                                with rclpy you can:
                                   ● Create and manage ROS 2 nodes that can communicate with other nodes in the ROS 2 ecosystem
                                   ● Publish messages to topics
                                   ● Subscribe to topics
                                   ● Provide and call services
                                   ● create and use actions
                                   ● Set timers
                                   ● Access paraeters
                                   ● Interact with the ROS 2 communication system
                                """

                                """
                                 Common rclpy functions:
                                    ● rclpy.init(args=None): Initializes the ROS 2 client library. This function must be called    before any other rclpy functions are used. It sets up the necessary resources for communication with the ROS 2 system.

                                    ● rclpy.shutdown(): Shuts down the ROS 2 client Library. This function should be called when your node is done using ROS 2 resources. It cleans up any resources that were allocated during initialization.

                                    ● rclpy.spin(node): enters a loop that keeps the node alive and responsive to incoming messages, service requests, and other events.

                                    ● Node: base class for creating ROS 2 nodes. It provides methods for publishing and subscribing to topics, providing and calling services, setting timers, and accessing parameters.

                                    ● create_publisher(msg_type, topic_name, qos_profile): creates a publisher for a specific message type and topic.

                                    ● create_subscription(msg_type, topic_name, callback, qos_profile): creates a subscription to a specific message type and topic, with a callback function that is called when a message is received.

                                    ● create_timer(timer_period_sec, callback): creates a timer that calls a specified callback function at a specified interval.

                                    ● get_logger(): returns a logger object that can be used to log messages at different severity levels (info, warning, error, etc.).

                                """
                                - <super().__init__('my_node')>
                                      # In Python, "super()"" is a built-in function that gives you access to methods and 
                                      #attributes of a parent (superclass) from within a child (subclass).

                                - <self.get_logger().info('my_node has started')>
                                      # Output log message to the console indicating that the node has started

                                - <rclpy.init(args=args)>
                                     # Initialize the ROS 2 client library. This function must be called before any other rclpy_functions are used.
                                     # It sets up the necessary resources for communication with the ROS 2 system.

                                - <rclpy.spin(node)>
                                     # keeps the node running and responsive to incoming messages, service requests, and other events.

                                - <try:
                                    ...
                                   except xxx:
                                     ...           
                                   finally:           
                                        ....>
                                        # 'finally' block is used for cleanup or guaranteed actions;
                                        # it always executes after the try block, regardless of whether an exception was raised or not.
## Notes for Future Students
     Task 1.Create student_robotics inside robot_ws/src using ament_python.
      Step 1:
            if 'robot_ws/src' not exist yet, create it first: <mkdir -p ~/robot_ws/src && cd ~/robot_ws/src>
           -'-p' 
              An option flag for the 'mkdir' command. It stands for parents.

              <mkdir -p> has two important behaviors:
                1. Creates parent directory (robot_ws) if they don't already exist

                2. Does not report an error if the directory already exists

      Step 2:
             -- "/opt/ros/<dostro>/setup.bash"
            "opt" is located at the root of the filesystem, not home directory

             How to check whether '/opt' exists:
             run <ls /> or directly run <ls /opt>
             -- execute the file: "setup.bash" in current shell

      Step 3:
              --ros2
              ROS 2 command line interface(CLI)

              --pkg
                stands for package; Tells ros2 tool you want to perform an operation related ROS packages

              --create
               tells ROS 2 to create a new package;

              It generates the necessary files and directory structure automatically; 
               Without this command, everything must be created manually

              -- '--build-type' stands for build type

              -- 'ament_python'
               
                 -ament
                    the offical build system used by ROS2

                    it is responsibilities:
                      ● Building packages
                      ● Installing packages
                      ● Managing package dependencies
                      ● Making packages discoverable by ROS 2

                  -ament_python(ament_cmake)
                   one of the build type; Telling ROS 2: this package contains python code. Build and install it using the python package system.

                  -package name: 'student_robotics'
___________________________________________________________________________________________________________________________________

      Task 2: Build the workspace and source the result
         
          Step 2:
                - colcon
                             a command-line build tool: (build and manage software projects that consist of multiple packages;
                                                             the standard build system for ROS 2 workspaces)
                                 colcon stands for: COLlECTIVE CONSTRUCTION

                              What colcon do:
                                    ● finds all packages in target directory

                                    ● Determines the dependency order

          Step 5:
                    ● ros2 
                           the ROS 2 command-line interface (CLI)
                    ● pkg
                          tells the CLI you want to work with packages.
                    ● list
                          lists all ROS 2 packages that ROS 2 can currently find

                    -- '|': called pipe: 
                      It takes the output of the command on the left and passes it as the input to the command on the right

                    -- 'grep'
                           searches text for lines that match a given pattern.

                    -- <grep student_robotics>
                     show only lines containing "student_robotics"

                     ⚠️ One thing the handbook flags as a common mistake: this source install/setup.bash step only applies to that terminal session. Every new terminal you open will need it re-sourced (or you can add it to your ~/.bashrc for convenience while developing).
__________________________________________________________________________________________________________________________________
         Task 3: Add a minimal node executable and run it through ros2 run

           Step 2:
                  --nano
                     'nano' is the command that starts the Nano text editor
                     Nano works entirely inside the terminal

                     A text editing screen will show up like:
                                                                      GNU nano 8.0                     New Buffer

                                                                      |

                                                                      ^G Help    ^O Write Out   ^R Read File
                                                                      ^X Exit    ^K Cut         ^U Paste
                                                                      ...                 
___________________________________________________________________________________________________________________________________
         
              