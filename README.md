Milestone 2.3 — Create Your First ROS 2 Package

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
   6. 
       ros2 run student_robotics my_node

   7.
       [INFO] [my_node]: my_node has started