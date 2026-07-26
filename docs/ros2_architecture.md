# ROS 2 Architecture Overview

- **Workspace** (`robot_ws`): the top-level folder that holds one or more packages and is built with `colcon`.
- **Package** (`student_robotics`): a unit of ROS 2 code — nodes, launch files, config — that lives inside the workspace's `src/`.
- **Node**: a single running process that does one job. Here, two nodes exist:
  - **Publisher node** (`talker`) — sends messages.
  - **Subscriber node** (`listener`) — receives messages.
- **Topic** (`/chatter`): a named channel nodes use to exchange messages. Publishers write to it; subscribers read from it. Neither node needs to know the other exists — they only need to agree on the topic name and message type.