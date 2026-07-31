•	What did I build?
        1. Milestone 2.1
          Resolved the integration and reproducibility issues identified in the final Week 1 engineering review. Recovered missing code if necessary, merged approved pull requests, cleaned the repository, and verified the final main branch from a fresh clone.

        2. Milestone 2.2
           Installed the appropriate ROS 2 distribution for my operating system, ran official verification examples, created a workspace, and wrrote a setup guide that another engineer can follow.

        3. Milestone 2.3
           Created a Python ROS 2 package named student_robotics. Inspected every generated file, removed nothing you do not understand, and documented the role of each important file.

        4. Milestone 2.4
           Implemented a publisher and subscriber inside student_robotics. The publisher sends a status message at a fixed rate. The subscriber receives and logs each message with enough information to verify communication.

        5. Milestone 2.5
             Polished student_robotics into a reusable example. Added a launch file, cleared configuration or parameters, architecture documentation, tests, and a troubleshooting section. Created another version of publisher that makes the parameters: publish rate and topic configurable.

•	Which milestone took the most time and why?
           Milestone 2.2 and milestone 2.3
           Because Installation of the ROS 2 distribution in my operating system(WSL) and creating first package involves many details/steps and I should make documents to record these steps and commands. So I spent much time to learn relevant commands including asking AI tools once I encountered commands I didn't understand.

•	What mistake did I repeat?
           I didn't repeat any mistake.

•	What was the most useful AI prompt?
           In milestone 2.5, after Claude code reviewed my package, 
           It reminded me some flaws in my package,two prompts is most useful.
            1. Missing runtime dependency declarations in package.xml. 
              I don't see <depend>rclpy</depend>, <depend>std_msgs</ depend>, <exec_depend>launch</exec_depend>, or <exec_depend>launch_ros</exec_depend>. It'll still build for you locally since those are almost certainly already on your machine, but a genuinely fresh environment following rosdep install --from-paths src --ignore-src -r -y wouldn't be told it needs them. Worth adding for the clean-clone test.

            2. One real (small) behavioral gap for your troubleshooting section:
               topic_name is only reconfigurable at launch time, not at runtime — if someone tries ros2 param set /status_publisher topic_name new_name while it's running, the parameter callback silently reports success but the publisher keeps using the original topic (only publish_rate has runtime-reconfigure logic). Not a bug relative to what the milestone requires, but it's the kind of "real error encountered" that belongs in your troubleshooting doc so the next intern doesn't waste time confused by it.

         Based on this two prompts, I added runtime dependencis in package.xml; and modified publisher(status_publisher_stretch) and subscriber(status_subscriber) after I understood these codes with Claude code's help.

•	What did I verify instead of assuming?
         ROS 2 distribution 

        Python ROS 2 package named "student_robotics"

        python file: "my_node.py"

        nodes: status_publisher, status_publisher_stretch and status_subscriber
         topic, publish rate(Hz)

        cleaner clone from the remote repo

•	What remains confusing?
         In milestone 2.3, 2.5 the file requires me wrote setup steps in README.md. In milestone 2.2 and 2.4, I was required to write setup files separately in the subdirectory 'docs'. When should I wrote setup information in a separate file and when I should write them in README.md file?

•	Can another engineer reproduce my work? What evidence proves this?
            Yes.
            From milestones 2.2-2.5, each milestone, I recorded information about how to do the mission in a setup file or 'README.md' file with plenty of detail information. So, another engineer can do it with the guide of these files. In the package: student_robotics, I wrote annotation for each segment of codes that might be difficult to understand for any new engineer.
