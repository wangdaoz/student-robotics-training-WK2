## Computer
   - Operating system: WSL 
   - Python version: Python 3.12.3
   - Git version: 2.43.0
   - VS Code installed: yes
   - Claude Code installed: yes

## Steps Completed && Commands Used
 #Step 1:
 Before installation, check what Ubuntu version WSL is running, since that determines which ROS 2 distro you can install — ROS 2 distros are  tied to specific Ubuntu LTS releases. Input the following instruction:
   -<lsb_release -a>     

 #Step 2. set locale:
  -<sudo apt update && sudo apt install -y locales>
 
  -<sudo locale-gen en_US en_US.UTF-8>

  -<sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8>

  -<export LANG=en_US.UTF-8>

#Step 3. Enable the Universe repo and add the ROS 2 apt source
    <sudo apt install -y software-properties-common curl gnupg2 lsb-release>

    <sudo add-apt-repository universe>

    <sudo apt update>

    <export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')>
    
    <curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME})_all.deb">

    <sudo dpkg -i /tmp/ros2-apt-source.deb>

    <rm /tmp/ros2-apt-source.deb>

#Step 4. Install ROS 2 (desktop includes RViz, demos, tutorials)
     <sudo apt update>

     <sudo apt upgrade -y>
       
     <sudo apt install -y ros-jazzy-desktop>


#Step 5. Install dev tools
     <sudo apt install -y ros-dev-tools>     

#Step 6. Source it (add to ~/.bashrc so it's automatic each terminal)
     <echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc>

     <source ~/.bashrc>
         executes the file in the current shell; reloads your updated .bashrc right away, so the current terminal gains the same ROS configuration without needing to be restarted.

Finally verify with the official talker/listener demo (matches Milestone 2.2's acceptance criteria) — open two WSL terminals:
     # Terminal 1
       <ros2 run demo_nodes_cpp talker>
   
     # Terminal 2
       <ros2 run demo_nodes_py listener>

#Step 7
Workspace(robot_ws):
       # 1. Create the workspace directory with a src/ subfolder
       <mkdir -p ~/robot_ws/src>

       <cd ~/robot_ws>

       # 2. Build the (currently empty) workspace with colcon
        <colcon build>

       # 3. Source the workspace overlay
           <source install/setup.bash>

        # 4. Verify it worked
             <printenv | grep -i AMENT_PREFIX_PATH>

## Problems encounted/trouble shooting
   1. After inputting  "sudo add-apt-repository universe", system asks me: adding component(s) 'universe' to all repositories?

      I asked the claude chat, then I know I should confirm with yes response. I typed 'y' and hit Enter

      That prompt is just "add-apt-repository" asking you to confirm before it edits your apt sources list (usually /etc/apt/sources.list or the files under /etc/apt/sources.list.d/) to add the universe component alongside main. It's a standard, safe step — universe is Canonical's community-maintained package repo, and several ROS 2 dependencies live there, so you need it enabled for the install to work.

    2. After opening two terminals to verify with the official talker/listener demo (matches Milestone 2.2's acceptance criteria),
       I didn't know how to exit a terminal.
       I asked the claude chat, it answers me to press "Ctrl+C" in each terminal: sends an interrupt signal that cleanly stops the running ROS 2 node.

    3. During the installation, I did not understand most commands. So I asked chatgpt to explain these commands in detail.

    4. I did not understand the concept "node", "service","action", underlay workspace, overlay workspace
       - Node: 
            basic unit of running a program in ROS 2 -- one process or a part of process;

            do a single, well-defined job and participates in the ROS 2 network

           Note strictly speaking, node ≠ process:
                        Usually one process runs one node, and that's a fine mental model for now. But ROS 2 does allow several nodes to share one process (called "composition") for efficiency.

       - Service:
                 A service is ROS 2's request/response communication pattern.

                 a two-way, on-demand exchange: 
                          client node: one node asks
                          Server node: another answers, and then the interaction is over

       - Action
            An action is ROS 2's pattern for long-running tasks — the ones where "ask and wait" isn't good enough because the task takes seconds or minutes, you want progress updates along the way, and you might need to abort it.

            Action has two roles: an action server and an action client
             But exchange has three parts
               1. Goal -- the client sends what it wants done ("drive to x=3, y=5"). The server explicitly accepts or rejects the  goal, so the client immediately knows whether the task even started.

               2. Feedback -- while working, the server streams progress updates, The client isn't blocked; it receives these asynchronously and can do other things meanwhile.

               3. Result -- when the task finishes, the server sends the final outcome, along with a status: succeeded, aborted, or canceled.

         - Underlay 
            the base environment — normally the system-wide ROS 2 installation you get from apt, activated with <source /opt/ros/<distro>/setup.bash>.

         - Overlay
              your own workspace (robot_ws) built on top of it. After building with colcon, you source the overlay's <install/setup.bash>, and its packages become visible in addition to everything in the underlay.

          Note: If a package with the same name exists in both, the overlay's version wins — it "shadows" the underlay copy. This is why the sourcing order matters, and it's exactly what the milestone's "why must a workspace be sourced after it is built" prompt is getting at: building produces the files, but sourcing is what tells your shell where to find them.

       5. what is "shell" in linux or WSL?
           I asked chatgpt. It provided me with detailed explaination.

           A shell is a program that provides the command-line interface (CLI) between you and the Linux operating system. It reads the commands you type, interprets them, and asks the operating system (the kernel) to execute them.

           In WSL (Windows Subsystem for Linux), when you open Ubuntu, you are usually placed into a shell such as Bash.

           Relationship between the shell and the kernel

           Here's the hierarchy:
                                        +--------------------------------------+
                                        |      Terminal: Your Commands         |
                                        |  ls, cd, mkdir, python, ros2, etc.   |
                                        +-----------------▲--------------------+
                                                          |
                                                          |
                                        +-----------------+--------------------+
                                        |               Shell                  |
                                        | (bash, zsh, fish, sh, etc.)          |
                                        | - Reads commands                     |
                                        | - Parses them                        |
                                        | - Starts programs                    |
                                        | - Manages variables                  |
                                        +-----------------▲--------------------+
                                                          |
                                                          |
                                        +-----------------+--------------------+
                                        |              Linux Kernel            |
                                        | - Manages CPU                        |
                                        | - Manages memory                     |
                                        | - Manages files                      |
                                        | - Manages devices                    |
                                        +-----------------▲--------------------+
                                                          |
                                                          |
                                        +-----------------+--------------------+
                                        |             Hardware                 |
                                        +--------------------------------------+
           The shell itself does not execute programs directly. 
           Instead, it asks the Linux kernel to create and run processes.

           after a user types a command, shell does following things:
            Waits for your input.
            Reads ls.
            Searches for the executable (/usr/bin/ls).
            Asks the kernel to start that program.
            Waits until it finishes.
            Displays another prompt.

          Other functions:
               1. navigate directories
               2. Create files
               3. Manage environment variables
               4. Redirect input and output
               5. Connect commands with pipes
               6. Run shell scripts
          Summary:
                 Terminal: the window where you type.
                 Shell (Bash): reads and interprets your commands.
                 Kernel: performs the actual operating system work.
                 Programs (ls, mkdir, python, ros2): launched by the shell through the kernel.

      6. during the installation, many commands were not understandable for me.
          
          1. -<lsb_release -a>     
           * lsb_release: A utility that reports Linux Standard Base (LSB) information about the operating system
           * -a: means "all", so it prints out all available distribution information

          ● Ubuntu 24.04 → ROS 2 Jazzy Jalisco (LTS, supported to May 2029) — most common choice right now, most tutorials/packages target it.
          ● Ubuntu 22.04 → ROS 2 Humble Hawksbill (LTS, supported to May 2027).
          ● Ubuntu 26.04 → ROS 2 Lyrical Luth (newest LTS, released May 2026) — only pick this if your packages/tutorials support it,  since it's new and the ecosystem is still catching up.

          2. -<sudo apt update && sudo apt install -y locales>
             <sudo apt update>
                ● sudo
                      ● Runs the command with administrator (root) privileges
                      ● Required because updating system packages affects the whole system
                ● apt
                      ● Ubuntu's package manager(Advanced Package tool)
                 It communicates with all configured software repositories, including:
               
                       ● Ubuntu Main

                       ● Ubuntu Universe

                       ● The ROS 2 repository you added earlier

                ● update
                     ● Downloads the latest package index from the configured software repositories.
                     ● It does not install or upgrade any software.
                     ● It simply refreshes the list of available packages.
              <sudo apt install -y locales>
                    ● sudo: ~
                    ● apt install
                         ● package manager installs the software package
                    ● -y
                       ● Automatically answers "Yes" to any confirmation prompts. without "-y" see something like:
                                                                                    Do you want to continue? [Y/n]
                    ● locales
                       The package containing locale data and tools such as:

                        ● locale-gen

                        ● locale configuration files

                        ● UTF-8 language definitions
                    ● joined two commands by "&&"
                       execute the second command only if the first command succeeds

         3. -<sudo locale-gen en_US en_US.UTF-8>
             ● locale-gen
                 ● Generates locale data from the definitions stored under /usr/share/i18n/
             ● en_US
                 ● English language for the United States
             ● en_US.UTF-8
                 ● English(United States) using UTF-8 encoding
              The command compiles these locales and stores them under: /usr/lib/locale/

         4. -<sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8>
                   ● update-locale
                      This utility writes locale settings into the system configuration file:/etc/default/locale

                   ● LC_ALL
                      LC_ALL has the highest priority among locale variables.
                      if LC_ALL is set:
                             LC_ALL
                                ↓
                             LC_TIME
                            LC_NUMERIC
                            LC_MESSAGES
                                ...
                                 ↓
                                LANG
                      so everything follows "LC_ALL"

                      It overrides:
                           date formatting
                           currency formatting
                           message language
                           sorting order
                           character encoding

                  ● LANG
                      default locale(language envrionment)
                      It tells programs:
                            ● use English
                            ● use UTF-8 encoding
         
         5. -<export LANG=en_US.UTF-8>
                set the locale for the current shell; Only affects current terminal session
     
                "export":
                     Creates or updates an environment variable and makes it available to child processes.
      
                "LANG=en_US.UTF-8":
                     sets the current shell's language

                   update-locale modifies the system's configuration for future login sessions, but it does not change the environment of your current shell.

                    That's why export LANG=en_US.UTF-8 is often run immediately afterward: it updates the current terminal so you don't have to log out and back in (or restart WSL) before the new locale takes effect.

         6. -<sudo apt install -y software-properties-common curl gnupg2 lsb-release>
             ● "software-properties-common": Gives you the add-apt-repository command used in the next step.

             ● "curl": A tool used to download files and interact with URLs from the terminal.

             ● "gnupg2": A tool for secure communication and verifying digital signatures (ensuring the ROS 2 software hasn't been       tampered with).

             ● "lsb-release": A utility that finds information about your specific Linux distribution (like your Ubuntu version name).

         7. -<sudo add-apt-repository universe>
             ● "add-apt-repository" is a command-line utility in Ubuntu that adds or enables software repositories

             ● Ubuntu divides its software into different "repositories." The Universe repository contains free and open-source software maintained by the Ubuntu community. ROS 2 relies on dependencies hosted here.

         8. -<sudo apt update>
               ● This tells your system to talk to all its registered repositories and fetch the latest list of available packages and their versions. It doesn't upgrade anything yet; it just updates the system's "shopping list."

         9. -<export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')>
            ● "ROS_APT_SOURCE_VERSION": temporary environment variable

            ● "curl -s ...": '-s': slient mode; sliently fetches data from given url about the newest version of the ROS repository setup tool

            ● "grep -F "tag_name"": 
                 * 'grep': search text 

                 * '-F': treat the search string literally

                 * find the line contains: tag_name":"0.4.2"

            ● awk -F\" '{print $4}'
         
                 * 'awk': process text by fields

                 * '-F\"': Sets the field separator to a double quote (").

                  "tag_name": "0.4.2" is split into fields 
                           | Field | Content  |
                           | ----- | -------- |
                           | $1    | (empty)  |
                           | $2    | tag_name |
                           | $3    | :        |
                           | $4    | 0.4.2    |

         10.-<curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/$  {ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME})_all.deb">

               'curl': download a file

               '-L' : follow HTTP redirects
                      GitHub download URLs often redirect to another server. Without '-L', 'curl' might stop at the redirect instead of downloading the file.

               '-o' : Specifies the output filename.
                      -o /tmp/ros2-apt-source.deb: 
                      save the download file as "/tmp/ros2-apt-source.deb"

               ${ROS_APT_SOURCE_VERSION}:
                  substitutes the environment variable.
                  suppose: ROS_APT_SOURCE_VERSION=0.4.2
                  then ${ROS_APT_SOURCE_VERSION} becomes 0.4.2

               `$(. /etc/os-release && echo ${UBUNTU_CODENAME})`
                 The '.' command (pronounced "source") executes the file in the current shell.
                 '/etc/os-release' contains variable such as:
                    NAME=Ubuntu
                    VERSION=24.04
                    UBUNTU_CODENAME=noble
                    After sourcing it, those variables become available in the current shell.

                    echo ${UBUNTU_CODENAME}: Prints the Ubuntu codename

         11. -<sudo dpkg -i /tmp/ros2-apt-source.deb>
            - dpkg 
               The low-level Debian package installer. Unlike apt, dpkg installs a package file that you already have on disk.

            - '-i': install
       
             The package configures your system to use the official ROS 2 APT repository by adding the appropriate repository configuration and trusted signing keys, so that future apt commands can install ROS 2 packages directly.

            <rm /tmp/ros2-apt-source.deb>
              - rm: remove

                  overall workflow:
     
                                                Install helper tools
                                                         │
                                                         ▼
                                            Enable the Universe repository
                                                         │
                                                         ▼
                                                 Refresh package lists
                                                         │
                                                         ▼
                                    Ask GitHub for the latest ROS apt source version
                                                         │
                                                         ▼
                                      Determine your Ubuntu codename (e.g., noble)
                                                         │
                                                         ▼
                                           Download the matching .deb package
                                                         │
                                                         ▼
                                             Install the package with dpkg
                                                         │
                                                         ▼
                                           Delete the temporary installer file
                                                         │
                                                         ▼
                          Your system is now configured to install ROS 2 packages using `apt`.

         12. -<sudo apt update>
               runs the command with administrator(root) privileges,
               Ubuntu's package manager downloads the latest package index from each repository
         13. -<sudo apt upgrade -y>

                Update all currently installed packages to their newest available versions

                Why upgrade before installing ROS?

             This is recommended because:

                   fixes bugs

                   installs security updates

                   ensures package dependencies are current
               
                   reduces the chance of dependency conflicts
       
         14 -<sudo apt install -y ros-jazzy-desktop>
             install ROS 2 Jazzy Desktop distribution, run the command with administrator(root) privileges

            -- "ros-jazzy-desktop"
                 the package name

              Ubuntu package names often follow the format:
                  ros-
                  distribution-
                  package
 
            -- desktop:
                   desktop package collection

             The package includes a complete desktop ROS 2 environment, such as:
                     Core ROS 2
                       ● rclcpp (C++ client library)
                       ● rclpy (Python client library)
                       ● ROS middleware (DDS)
                       ● communication libraries
                     ________________________________________

                       Visualization
                         ● RViz2

                         Used to visualize:
                          ● robots
                          ● LiDAR scans
                          ● cameras
                          ● maps
                          ● coordinate frames
                          ● planned paths

                        _________________________________________

                      Simulation support
                        Tools that integrate with simulators like Gazebo, along with message types and utilities commonly used in simulation workflows.
                     _____________________________________________________________

                      Common ROS messages

                      Packages defining standard message types, for example:

                         ● std_msgs
                         ● geometry_msgs
                         ● sensor_msgs
                         ● nav_msgs
                         ● visualization_msgs
                       These provide common data structures used for communication between ROS nodes.
                     _______________________________________________________________________________________

                      Command-line tools
                       Utilities such as:
                         ros2
                       user can use:
                         ● ros2 topic list
                         ● ros2 node list
                         ● ros2 service list
                         ● ros2 run
                         ● ros2 launch
                     __________________________________________________________________________________________

                     Tutorials and demos
                      example programs to help you learn ROS 2.

                     ___________________________________________________________________________________________

                     Build tools
                      Tools for compiling ROS workspaces, such as:

                            ● colcon
                            ● CMake support
                            ● Python packaging support
                     ____________________________________________________________________________________________

              What happens internally?

                                                         ros-jazzy-desktop
                                                                 │
                                                                 ├── rclcpp
                                                                 ├── rclpy
                                                                 ├── rviz2
                                                                 ├── tf2
                                                                 ├── ros2cli
                                                                 ├── geometry_msgs
                                                                 ├── sensor_msgs
                                                                 ├── nav_msgs
                                                                 ├── visualization_msgs
                                                                 ├── demo_nodes_cpp
                                                                 ├── demo_nodes_py
                                                                 └── ... (hundreds of additional packages)
            
             Overall Workflow:
                                                          sudo apt update
                                                                │
                                                                ▼
                                     Refresh the package lists from all configured repositories
                                                                │
                                                                ▼
                                                         sudo apt upgrade -y
                                                                │
                                                                ▼
                                       Update existing software to the latest compatible versions
                                                                │
                                                                ▼
                                                sudo apt install -y ros-jazzy-desktop
                                                                │
                                                                ▼
                                    Download and install the complete ROS 2 Jazzy Desktop environment,
                                           including the core ROS libraries, RViz2, command-line tools,
                                           standard message packages, tutorials, and their dependencies.

        15 -<sudo apt install -y ros-dev-tools>
          -- ros-dev-tools
             Package to install tools used to develop ROS software

             A meta-package. It doesn't contain much software itself but depends on a collection of development tools.

             | Tool                   |            Purpose                                      |
             | ---------------------- | ------------------------------------------------------- |
             | `colcon`               | Build ROS workspaces                                    |
             | `vcstool`              | Download multiple Git repositories from a `.repos` file |
             | `rosdep`               | Install system dependencies required by ROS packages    |
             | `ament_lint`           | Run code quality and style checks                       |
             | `python3-rosdep`       | Python interface for `rosdep`                           |
             | Other helper utilities | Tools commonly used during ROS development              |

         16 -<echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc>
            --echo:
                print text to the terminal

              appends a line: "source /opt/ros/jazzy/setup.bash" to your "~/.bashrc" file
              Note: You should make sure the location of the .bashrc and write the exact file path

         17 -<source ~/.bashrc>
              executes the file in the current shell; reloads your updated .bashrc right away, so the current terminal gains the same ROS configuration without needing to be restarted.

         18 -<ros2 run demo_nodes_cpp talker>
           -- ros2
              main command-line tool; provides many subcommands such as:
                                           ros2 node
                                           ros2 topic
                                           ros2 service
                                           ros2 action
                                           ros2 launch
                                           ros2 run
           -- run
              run a executable from a installed package

           -- demo_nodes_cpp
                a package contains demonstration programs written in C++

           -- talker
               an executable inside the package, a C++ program; after start, repeatedly publish messages

         19 -<ros2 run demo_nodes_py listener>

            -- demo_nodes_py
               package containing python demo programs

            -- listener
                an executable inside the package, it receives messages
    
            If you see the talker publishing and the listener printing what it hears, the install is verified.

          Note: 
               RViz/GUI apps need an X server or WSLg (built into recent Windows 11) — if rviz2 fails to open a window, that's usually the cause

         20 -<mkdir -p ~/robot_ws/src>
              -- '-p'
                 1. Create parent directories if they don't already exist
                 2. don't report an error if the directory already exists
         21 -<cd ~/robot_ws>
               access to the workspace directory robot_ws

         22 -<colcon build>
           - colcon
               a command-line build tool: (build and manage software projects that consist of multiple packages;
                                         the standard build system for ROS 2 workspaces)
               colcon stands for: COLlective CONstruction

              What colcon do:
                 ● finds all packages in target directory

                 ● Determines the dependency order

         23 -<source install/setup.bash>
              -- source: a built-in command. it executes the commands in current shell not a new shell

              -- install/setup.bash
                 After running <colcon build>
                 in workspace folder "robot_ws", a sub directory "install", a file "setup.bash" inside it; is a script generated during the build. It prepares your shell to use the packages in this workspace. It updates several environment variables that ROS 2 uses.

         24 -<printenv | grep -i AMENT_PREFIX_PATH>

             --printenv
                 Linux command that prints all environment variables in the current shell

             -- '|': called pipe: 
                       It takes the output of the command on the left and passes it as the input to the command on the right

             -- 'grep'
                 searches text for lines that match a given pattern.

             -- '-i'
                 thie option means ignore the uppercase or smaller case

             -- 'AMENT_PREFIX_PATH': an ROS 2 environment variable
                  it tells the ROS 2 where to look for installed package
                  search workspace first; search for system-wide ROS 2 installation

## Notes for Future Students
     RViz/GUI apps need an X server or WSLg (built into recent Windows 11) — if rviz2 fails to open a window, that's usually the cause