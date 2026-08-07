# ROS 2 Architecture Overview

- **Workspace**
    What: 
     the top-level folder/ a developmet environment that holds one or more packages and is built with `colcon`.

    Why exits:
     A robot system is often composed by many software; Each has its own package. ROS should group them into one workspace so build and package discovery is much easier.
     
     Project example:
          student-robtics-training-WK2/robot_ws/

     Beginner Common Mistake:

        Beginners usually think that workspace is the direct directory or development environment for software development;

        Most beginners do not know the essential for workspace is top-level folder or top-level environment.

- **Package**
   What:
        a reusable unit of ROS 2 sortware containing nodes, launch files and configuration

   Why exists:
          A package exists to organize, build, share, and reuse related robot software as a single unit.

   Project Example:
         'student_robotics' in the directory: robot_ws/src/

   Beginner Common Mistake:
            
              Beginner often thinks that a package in a workspace only contains program files; don't know that a package can contain other type of files (launch file, text files ...)


- **Node** 
         basic unit of running a program in ROS 2 -- one process or a part of process;
         a running ROS 2 software component that performs a focused job

      Why exists:
            Each software in a robot system must contain one or more executables(programs) required to run for specific jobs;

      Project Example:
              Publisher node: (`status_publisher`) — sends messages.
              Subscriber node: (`status_subscriber`) — receives messages.
      
      Beginner Common Mistake:
         
         Often think a node is equivalent to a process and ignore that a node can be a component/part of a focused job.
      
- **Topic**
    What:
      a named channel that nodes use to exchange messages. Publishers write to it; subscribers read from it. Neither node needs to know the other exists — they only need to agree on the topic name and message type.

    Why exists:
       A topic exists to allow nodes to communicate without needing to know about each other. This makes robotic software modular, flexible, and scalable.

    Project Example:
       In my project, the topic: `/robot_status` is a channel for publisher node and subscriber node to communicate with each other.

    Beginner Common Mistake:
        
        Only understand "Topic" literally; Beginners only understand 'topic' in a lowest level that it is the main topic that nodes communicate with other node.

- **Message**
    What:
          the defined data type or date structure carried by a topic 

    Why exists:
      A message provides a common language/ pattern that all nodes agree on.

    Real Example:
       publisher node send a message with a string data contains: sequence number of current node and the elapsed time to send the message.
    
    Beginner Common Mistake:
       Beginners can not think any message is a data type defined by a topic. They often narrow the message to a string type data.
    

- **Service"
    What:
      A service is ROS 2's request/response communication pattern. A client sends a request to a server; Server send a response to the client.

    Why exists:
       Avoid server sending a message repeatedly on a channel

    Real Example:
           For a publisher node, in a given publish rate(time period), once one message is sent, the sequence number of message will increased by one, the start time and elapsed time will be recomputed to generate a new message.

           For a subscribe node, once it receives a message from the topic, the message will be added to the queue (Qos) and the subscriber will continue to receive next message.

    Beginner Common Mistake:
         Think the service is used for continuous sensor data, which is exactly what topics/channels for.

- **action**
    What:
         An action is a ROS 2 pattern for long-running tasks. The pattern includes tow roles: action server and action client. The exchange includes three parts: Goal, feedback, result.

    Why exists:
         This pattern allows action server notify the progress and result of a task to an action client from the begining to the end.

    Real Example:
         Order a commodity in Amazon, you place order. Amazon platform shows the status: Ordered; Next show the status: Shipped; Then, platform shows the status: Out for delivery. Finally, it shows the status: Delivered

    Beginner Common Mistake:
         A beginner ususally thinks that an action is what the server or client does in a specific task. For example, the publisher sends a message to the topic and the subscriber listens to the 'topic' and receives relevant messages. 

         The action is a ROS 2 pattern used in long-running tasks.

- **launch file**
    What:
       A python file: how multiple nodes are started and configured together

    Why exists:
       A robot often has many nodes; If starting running them individually, the efficiency is pretty low. The launch file is used to start running these nodes automatically.

    Real Example:
         "status_demo.launch.py" runs publisher and subscriber respectively.

    Beginner Common Mistake:
    
       Think absolutely that a launch file must start all nodes together. Actually, it might start these nodes in some sequence.

       Think a launch file contains robot logic. Actually, they only describle how to start the system in a robot.

- **Parameters**
    What:
      configuration values inside nodes

    Why exist:
       many arguements in should of be changed by users. Without files these arguements should be hardcoded in source files, then rebuild and restart. With parameters, input command: <ros2 param set /nodename parameters xxx>, reset is done.

    Real Example:
       the publish rate and topic

    Beginner Common Mistake:
        variables in source files can only be hardcoded. Parameters make nodes reusable.

- **colcon**
   What:
        A command line build tool: build and manage software projects that consist of multiple packages; the standard build system for ROS 2 workspaces

   Why exists:
      Suppose there are multiple packages in a target directory and a certain dependency order among these packages. Manully building is impossible. Colcon can make a collective construction with following tasks:
                                                                    ● determines dependency order
                                                                    ● compiles packages
                                                                    ● installs packages
                                                                    ● generates environment setup files
   
   Real Example:
         in directory: ~/student-robotics-training-WK2/robot_ws, inputted <colcon build> to wuild all packages.

   Beginner Common Mistake:
         Think colcon is a part of ROS 2 (protocol)

         In fact, ROS 2 uses colcon as a build tool.
      
- **Underlay**
      What:
           The existing ROS environment already installed on computer      

      Why exists:
        every project needs common libraries instead of copying them in each workspace. ROS 2 installs them once.

      Real Example:
         In a fresh new terminal, input command: <source /opt/ros/jazzy/setup.bash> to install ROS 2 environment in current terminal

      Beginner Common Mistake:
        build ROS itself inside every workspace, which is unnecessary.

- **Overlay**
      What:
         Workspace layered on top of the underlay(ROS environment)
      
      Why exists:
        Allow users to create their own workspaces; ROS 2 will use these workspaces first, which keeps the system installation untouched while letting you customize or replace packages.

      Real Example:
         workspace directory: robot_ws, after inputting command <source install/setup.bash>

      Beginner Common Mistake:
         forget to source the overlay(<source install/setup.bash>) after editing files in one or more packages in the workspace; Without doing this, ROS only sees the underlay, so your newly built packages may appear to be "missing."


          