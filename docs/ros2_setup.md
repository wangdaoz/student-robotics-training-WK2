Before installation, check what Ubuntu version WSL is running, since that determines which ROS 2 distro you can install — ROS 2 distros are  tied to specific Ubuntu LTS releases. Input the following instruction:
    <lsb_release -a>  
  ● Ubuntu 24.04 → ROS 2 Jazzy Jalisco (LTS, supported to May 2029) — most common choice right now, most tutorials/packages target it.
  ● Ubuntu 22.04 → ROS 2 Humble Hawksbill (LTS, supported to May 2027).
  ● Ubuntu 26.04 → ROS 2 Lyrical Luth (newest LTS, released May 2026) — only pick this if your packages/tutorials support it,  since it's new and the ecosystem is still catching up.

#1. set locale:
     <sudo apt update && sudo apt install -y locales>
     <sudo locale-gen en_US en_US.UTF-8>
     <sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8>
     <export LANG=en_US.UTF-8

#2. Enable the Universe repo and add the ROS 2 apt source
    <sudo apt install -y software-properties-common curl gnupg2 lsb-release>
    <sudo add-apt-repository universe>
    <sudo apt update>
    <export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')>
    <curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME})_all.deb">
    <sudo dpkg -i /tmp/ros2-apt-source.deb>
    <rm /tmp/ros2-apt-source.deb>

#3. Install ROS 2 (desktop includes RViz, demos, tutorials)
    <sudo apt update>
    <sudo apt upgrade -y>
    <sudo apt install -y ros-jazzy-desktop>

#4. Install dev tools
     <sudo apt install -y ros-dev-tools>

#5. Source it (add to ~/.bashrc so it's automatic each terminal)
     <echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc>
     <source ~/.bashrc>

Finally verify with the official talker/listener demo (matches Milestone 2.2's acceptance criteria) — open two WSL terminals:
     # Terminal 1
       <ros2 run demo_nodes_cpp talker>

     # Terminal 2
      <ros2 run demo_nodes_py listener>
    
    If you see the talker publishing and the listener printing what it hears, the install is verified.

Note: 
       RViz/GUI apps need an X server or WSLg (built into recent Windows 11) — if rviz2 fails to open a window, that's usually the cause


Workspace(robot_ws):
       # 1. Create the workspace directory with a src/ subfolder
       <mkdir -p ~/robot_ws/src>
       <cd ~/robot_ws>

       # 2. Build the (currently empty) workspace with colcon
        <colcon build>

       # 3. Source the workspace overlay
           <source install/setup.bash>
     
  A few things worth understanding as you do this (the milestone wants you to be able to explain, not just run commands):
     1. Why src/ specifically? colcon expects your packages to live inside src/. It scans that folder, builds each package it finds, and puts the results in sibling build/, install/, and log/ directories that it creates automatically at the workspace root.

     2. Why build before there's anything in src/? It's a sanity check — confirms colcon and your ROS 2 install are working correctly before you add real packages. You should see output like "Summary: 0 packages finished" since src/ is empty.

     3. Why source it after building? Sourcing "install/setup.bash" adds this workspace's packages to your shell's ROS 2 environment (updates "AMENT_PREFIX_PATH" and similar variables) so "ros2 run" and "ros2 pkg list" can find anything you build here. This is the "underlay/overlay" concept from your Concepts to Explore list: "/opt/ros/jazzy/setup.bash" (sourced earlier) is your underlay, and "robot_ws"'s "install/setup.bash" is an overlay on top of it — you source the underlay first, then the overlay, so the overlay's packages take priority while still having access to everything in the underlay.

  Verify it worked:
     # Confirm the workspace env is active
       <printenv | grep -i AMENT_PREFIX_PATH>

