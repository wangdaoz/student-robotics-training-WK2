import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kevin-lianhu/student-robotics-training-WK2/robot_ws/install/student_robotics'
