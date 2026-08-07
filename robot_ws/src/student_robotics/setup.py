import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'student_robotics'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kevin-lianhu',
    maintainer_email='wangdaoz@oregonstate.edu',
    description='Student robotics training package with a minimal ROS 2 node.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [   
            'my_node = student_robotics.my_node:main',
            'status_publisher = student_robotics.status_publisher:main',
            'status_publisher_stretch = student_robotics.status_publisher_stretch:main',
            'status_subscriber = student_robotics.status_subscriber:main',
        ],
    },
)
