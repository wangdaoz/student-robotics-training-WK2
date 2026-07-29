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

## Milestone 2.5 task 2



  Expected Results:
        [INFO] [launch]: Default logging verbosity is set to INFO
        [INFO] [status_publisher_stretch-1]: process started with pid [5320]
        [INFO] [status_subscriber-2]: process started with pid [5321]
        [status_subscriber-2] [INFO] [1785271286.446624919] [status_subscriber]: Status Subscriber Node has started.
        [status_publisher_stretch-1] [INFO] [1785271286.446686811] [status_publisher]: Status publisher started at 1.0 Hz.
        [status_publisher_stretch-1] [INFO] [1785271287.423258444] [status_publisher]: Publishing: "seq=0, elapsed=1.00s"
        [status_subscriber-2] [INFO] [1785271287.423980855] [status_subscriber]: Received status message: "seq=0, elapsed=1.00s"
        [status_publisher_stretch-1] [INFO] [1785271327.784233185] [status_publisher]: Publishing: "seq=1, elapsed=41.36s"
        [status_subscriber-2] [INFO] [1785271327.786151927] [status_subscriber]: Received status message: "seq=1, elapsed=41.36s"
        [status_publisher_stretch-1] [INFO] [1785271328.516016717] [status_publisher]: Publishing: "seq=2, elapsed=42.09s"
        [status_subscriber-2] [INFO] [1785271328.516446948] [status_subscriber]: Received status message: "seq=2, elapsed=42.09s"
        [status_publisher_stretch-1] [INFO] [1785271329.422937935] [status_publisher]: Publishing: "seq=3, elapsed=43.00s"
        [status_subscriber-2] [INFO] [1785271329.423004997] [status_subscriber]: Received status message: "seq=3, elapsed=43.00s"
        [status_publisher_stretch-1] [INFO] [1785271330.423615806] [status_publisher]: Publishing: "seq=4, elapsed=44.00s"
        [status_subscriber-2] [INFO] [1785271330.424709514] [status_subscriber]: Received status message: "seq=4, elapsed=44.00s"