## run 'status_publisher.py'
   
   <colcon build --packages-select student_robotics>: 
       tell the the ROS 2 build tool 'colcon' to build the package: student_robotics

   <source install/setup.bash>: 
       add newly built package to ROS 2's search path for the current terminal session

   <ros2 run student_robotics status_publisher>
         tell the ROS 2 command line interface to run the file: status_publisher inside the package called student_robotics

    Expected Results:
             [INFO] [1784942486.499802557] [status_publisher]: Status publisher node has started.
             [INFO] [1784942487.487484295] [status_publisher]: Publishing: "Robot is operational. Sequence number: 0, Elapsed time: 1.00 seconds" 
                         .
                         .
                         .

## run 'status_subscriber.py'
   Supposed that the file 'status_publisher.py' is running

   <colcon build --packages-select student_robotics>: 
       tell the the ROS 2 build tool 'colcon' to build the package: student_robotics

   <source install/setup.bash>: 
       add newly built package to ROS 2's search path for the current terminal session

   <ros2 run student_robotics status_subscriber>
         tell the ROS 2 command line interface to run the file: status_subscriber inside the package called student_robotics

    Expected Results:
              [INFO][......][status_subscriber]: Status Subscriber Node has started.
              [INFO][......][status_subscriber]: Received status message: "Robot is operational. Sequence number: 0, Elapsed time: 1.00 seconds"
                                         .
                                         .
                                         .