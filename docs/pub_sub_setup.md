## Computer
    ● Operating system: WSL

    ● Python version: Python 3.12.3

    ● Git version: 2.43.0

    ● VS Code installed: yes

    ● Claude Code installed: yes

## Steps Completed && Commands Used
    
    Step 1: Open 3 terminals and source all terminals
    
       ● <source /opt/ros/<distro>/setup.bash>

        Note: Replace <distro> with whatever ROS 2 version you installed in Milestone 2.2 (e.g. humble, jazzy, iron). Worth checking with <echo $ROS_DISTRO> to confirm it's already sourced.
       
       ● <source ~/student-robotics-training-WK2/robot_ws/install/setup.bash>
               add built package to ROS 2's search path for current terminal session

    Step 2: run Publisher file in first terminal

        <ros2 run student_robotics status_publisher>

        Expected Results:
             The status_publisher.py run nomrally, send robot status messages to the topic and outputs them in terminal respectively.

    Step 3: run Subscriber file in next terminal
        <ros2 run student_robotics status_subscriber>
         
        Expected Results:
         The subscriber node starts, receive messages from topic and outputs them in terminal respectively

    Step 4: Input Inspection commands in the remind terminal
        
        # 1. confirms the topic actually exists on the network:
           <ros2 topic list>:
           Tell the ROS 2 CLI, I you want to work with topics, list all ROS 2 packages that ROS 2 can current find
        
         Expected Results:
           You should see /robot_status in the output (along with some default topics like /parameter_events, /rosout). If /robot_status isn't listed, the publisher isn't running or isn't sourced correctly — nothing downstream will work

        # 2. prints every message as it arrives, straight from the topic itself
             <ros2 topic echo /robot_status>
             
             Expected Results:
                 data: 'seq=7, elapsed=7.01s'
                 ---
                 data: 'seq=8, elapsed=8.01s'
                 ---

             This is a third independent listener — proof that the topic is genuinely broadcasting, not just that your specific subscriber node happens to be printing something. Ctrl+C to stop it when you're done. 

        # 3. measures the actual publish rate, to confirm it's really ~1 Hz and not just "close enough by eye"
             <ros2 topic hz /robot_status>
             Expected Results:
               average rate: 1.000
                   min: 0.999s max: 1.001s std dev: 0.00043s window: 10
             Run it for a while until enough samples to average then press "Ctrl+C"

## Notes for Future Students
    Step 1: 
       
             -- "/opt/ros/<dostro>/setup.bash"
            "opt" is located at the root of the filesystem, not home directory

             How to check whether '/opt' exists:
             run <ls /> or directly run <ls /opt>
             -- execute the file: "setup.bash" in current shell

             -- <source ~/student-robotics-training-WK2/robot_ws/install/setup.bash>
               add built package to ROS 2's search path for current terminal session