from setuptools import find_packages, setup

package_name = 'student_robotics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kevin-lianhu',
    maintainer_email='wangdaoz@oregonstate.edu',
    description='Student robotics training package with a minimal ROS 2 node.',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [   'my_node = student_robotics.my_node:main',
        ],
    },
)
