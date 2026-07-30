## Purpose
     Milestone 2.3 — Create Your First ROS 2 Package

## Repository Structure
           student-robotics-training-WK2/
           ├── README.md
           ├── docs/
           │   ├── ros2_setup.md
           │   ├── ros2_architecture.md
           │   └── weekly_report_week2.md
           ├── robot_ws/
           │   └── src/
           │       └── student_robotics/
           ├── tests/
           ├── config/
           └── .gitignore

## Setup
 ### Build Package "student_robotics"
  1. Make sure you're inside your workspace's "src" directory
      <cd ~/robot_ws/src>
      (If robot_ws/src doesn't exist yet, create it first: <mkdir -p ~/robot_ws/src && cd ~/robot_ws/src>)

  2.  Make sure ROS 2 is sourced
      <source /opt/ros/<distro>/setup.bash>
       check it is sourced: <echo $ROS_DISTRO>

  3. Run the package creation command
      <ros2 pkg create --build-type ament_python student_robotics>

       the folder structure like:
         student_robotics/
          ├── package.xml
          ├── setup.py
          ├── setup.cfg
          ├── resource/
          │   └── student_robotics
          ├── student_robotics/
          │   └── __init__.py
          └── test/
  
 ### Build the workspace and source it
 1. go to the workspace ~/robot_ws

 2. <colcon build>

 3. check what the build created
     robot_ws/
      ├── build/
      ├── install/
      ├── log/
      └── src/

 4. source install/setup.bash
        <source install/setup.bash>

        This adds your newly built package to ROS 2's search path for the current terminal session, so commands like <ros2 pkg list> or <ros2 run> can find student_robotics

 5. Verify it's discoverable
       <ros2 pkg list | grep student_robotics>
       If "student_robotics" shows up, the build and source worked.
    ⚠️ One thing the handbook flags as a common mistake: this source install/setup.bash step only applies to that terminal session. Every new terminal you open will need it re-sourced (or you can add it to your ~/.bashrc for convenience while developing).
      <nano ~/ .bashrc>
      <source /opt/ros/<distro>/setup.bash>:
      Replace <distro> with your actual ROS 2 distribution (e.g. humble, jazzy, iron), and adjust the path if your workspace isn't at ~/robot_ws.

      In nano: Ctrl+O, then Enter, then Ctrl+X
      In vim: Esc, then :wq, then Enter

 ### Add a minimal node executable and run it through ROS 2
   1. 
       <cd ~/student-robotics-training-WK2/robot_ws/src/student_robotics/student_robotics>
   2. 
       <nano my_node.py>
   3. 
       <cd ..>
       <nano setup.py>
   4. 
       <cd ~/student-robotics-training-WK2/robot_ws>
       <colcon build>
   5.
       source install/setup.bash
 

 ## Running Examples
         "my node.py"

## Testing
       <ros2 run student_robotics my_node>

       Expected Results:

       [INFO] [my_node]: my_node has started

## Current Status
    package build/, install/, log/, src/ were created in "student-robotics-training-WK2/robot_ws/" directory
    insider the directory 'src', a new package was created:
                                  student_robotics/
                                    ├── package.xml
                                    ├── setup.py
                                    ├── setup.cfg
                                    ├── resource/
                                    │   └── student_robotics
                                    ├── student_robotics/
                                    │   └── __init__.py
                                    |   └── my_node.py
                                    └── test/

## Next Steps
   Milestone 2.4 Build Your First Distributed Robotics Software
   Milestone 2.5 Build a Reusable ROS 2 Onboarding Example

___________________________________________________________________________________________________________________________________

## Purpose
    Milestone 2.5 Build a Reusable ROS 2 Onboarding Example

## Repository Structure

## Setup

    Tasks
      
        #1 Add one launch command that starts publisher and subscriber together.
           
            access to the directory of your workspace
            <cd ~/<Username>/student-robotics-training-WK2/robot_ws>
              Note: replace <Username> with your actually username

             Add a launch file:
              <touch src/student-robotics/launch/status_demo.launch.py>
               
               --touch create a new, empty file with a given name
             Rebuild the package and resource it in current shell
             
               <colcon build --packages-select student_robotics>

               <source install/setup.bash>
                read and execute the commands in given scripts inside the current shell
                the script configures your shell by updating several environment variables.

                 For example, it tells ROS 2 things like:

                    Where your packages are installed.
                    Where executables are located.
                    Where launch files are located.
                    Where message definitions are located.
                    Where Python modules are located.

        #2 Make at least one behavior configurable, such as publish rate or topic name.
             Suppose you want to make both publish rate and topic name configurable:

               1. modify codes in "status_publisher_stretch.py"
                   add the following codes:
                       <self.declare_parameter('publish_rate', 1.0)>
                       <self.declare_parameter('topic_name', 'robot_status')>

                        -- declare_paramter(xxx,xxx)
                            This is a method inherited from the "Node" class
                            It's role is to tell the ROS:
                                                          my node has a parameter with a given name
                            
                            the basic syntax: <self.declare_parameter(parameter_name, default_value)>
                              
                               ● parameter_name is a string

                               ● default_value is the value used if no other value is supplied

                       <publish_rate = self.get_parameter('publish_rate').get_parameter_value().double_value>
                        
                        -- self: current object

                        -- get_parameter('publish_rate')
                            return a Parameter object named 'publish_rate'

                        -- get_parameter_value()
                           return corresponding object: ParameterValue

                        -- double_value
                           the object: ParameterValue contains fields for every ROS parameter type,
                           since 'publish_rate' is float so extract it from  the 'double_value' field 
                        
                       <topic_name = self.get_parameter('topic_name').get_parameter_value().string_value>

                 after the following codes:
                           "class StatusPublisher(Node):
                               def __init__(self):
                                   super().__init__('status_publisher')"

               2. modify codes in "status_subscriber.py"
                   After the segment of codes <"class StatusSubscriber(Node):
                                                  def __init__(self):
                                                      super().__init__('status_subscriber')">
                    Add codes:
                               <self.declare_parameter('topic_name', 'robot_status') # Declare a parameter for the topic name
                                topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        
                                # subscription: topic name: 'robot_status', message type: callback, queue size(Qos depth):
                                self.subscription = self.create_subscription(String, topic_name,
                                self.listener_callback, 10)>
                    Note: standard identification is 4 space otherwise, the termianl wiil report stderr about identification
                3. Modify the launch file
                   In your launch file:
                      modify original contents into the current version of code:
                         [ 
                            from launch import LaunchDescription
                            from launch.actions import DeclareLaunchArgument
                            from launch.substitutions import LaunchConfiguration
                            from launch_ros.actions import Node

                            def generate_launch_description():
                                publish_rate_arg = DeclareLaunchArgument('publish_rate', default_value='1.0')
                                topic_name_arg = DeclareLaunchArgument('topic_name', default_value='robot_status')

                                publisher_node = Node(
                                    package='student_robotics',
                                    executable='status_publisher_stretch',
                                    name='status_publisher',
                                    parameters=[{
                                        'publish_rate': LaunchConfiguration('publish_rate'),
                                        'topic_name': LaunchConfiguration('topic_name'),
                                    }]
                                )

                                subscriber_node = Node(
                                    package='student_robotics',
                                    executable='status_subscriber',
                                    name='status_subscriber',
                                    parameters=[{'topic_name': LaunchConfiguration('topic_name')}]
                                )

                                return LaunchDescription([publish_rate_arg, topic_name_arg, publisher_node, subscriber_node])
                         ]
                         
                 

                4. rebuild the package and source it in current shell
                     
                     <colcon build --packages-select student_robotics>

                     <source install/setup.bash>
                       read and execute the commands in given scripts inside the current shell
                       the script configures your shell by updating several environment variables.
        
        #5 Add a verification script
            # script
              1. create a bash file: <touch ~/student-robotics-training-WK2/tests/verify_demo.sh>

              2. Suppose you're in your repo and finished editing the scripts,
                  <chmod +x tests/verify_demo.sh>
                  --chmod
                     change file's permissions

                  -- '+x'
                     add the execute permission
                     Without it, the file is just text — Linux won't let you run it directly, and ./tests/verify_demo.sh will fail with "Permission denied." After chmod +x, the file is marked executable, and since it starts with #!/bin/bash (the shebang line), the system knows to run it with bash when you invoke it directly


                   
## Running Examples
      1. robot_ws/src/student_robotics/launch/status_demo.maunch.py
      2. robot_ws/src/student_robotics/student_robotics/status_publisher_stretch.py
      3. robot_ws/src/student_robotics/student_robotics/status_subscriber.py

## Testing
   Task 1:
    Case 1: in built-in terminal
             <ros2 launch student_robotics status_demo.launch.py>

             -- ros2 invokes the ROS 2 command-line interface

             -- launch tell the ROS 2 to run a launch file

             -- <packagename>: the package containing the file

             -- <launch_file> is the python launch file to execute

    
     Case 2: in a new terminal window
            
             <env -i HOME="$HOME" TERM="$TERM" bash --norc --noprofile> (optional)

              --env a Linux utility for working with environment variables

              -- '-i' ignore the current environment

              -- HOME="$HOME"
                   "Create a new environment variable named HOME whose value is the same as my current HOME.

              -- TERM="$TERM"
                     copies your current terminal type.

              -- bash
                  starts a new bash shell

              -- '--norc'
                Normally, when Bash starts interactively, it reads: ~/.bashrc

                '--norc' tells Bash: Do not read '~/.bashrc'
                So none of those customizations are applied.

              -- '--noprofile' 
                  When Bash starts as a login shell, it normally reads one of: '~/.bash_profile' or '~/.profile'

                  These files often contain commands like:
                                         export PATH=...
                                         source /opt/ros/jazzy/setup.bash

                 '--noprofile' tells bash: "Ignore all login startup files."

             <source /opt/ros/jazzy/setup.bash>
               Read and execute the given script in current shell

               Role: Configure my current terminal to use the system-wide ROS 2 Jazzy installation by executing its setup script, so ROS 2 commands (ros2), packages, libraries, and Python modules are available in this shell."

              <source ~/robot_ws/install/setup.bash>
                 Read and execute the setup.bash script generated by colcon in the current shell so that this terminal knows about all the ROS 2 packages, executables, launch files, and Python modules installed in my workspace."

            <ros2 launch student_robotics status_demo.launch.py>

            Open another terminal, source it as mentioned above, input following commands respectively

            <ros2 node list>

            <ros2 topic list>

            <ros2 topic hz /robot_status>
            
            <ros2 param get /status_publisher publish_rate>

   Task 2:
            1. input the commands: 
                  <ros2 launch student_robotics status_demo.launch.py publish_rate:=2.0 topic_name:=robot_status_test>
                   in current terminal

            2. in a new terminal:
                      <source /opt/ros/jazzy/setup.bash>

                      <source ~/robot_ws/install/setup.bash>

                      <ros2 topic list> or <ros2 topic hz /robot_status_test> or <ros2 topic echo /robot_status_test>
                       
                      If messages show up on rename topic and reset publish rate, both nodes correctly picked up the same override.
                
   Task 5:
          <./tests/verify_demo.sh>

                
## Current Status

## Next Steps
