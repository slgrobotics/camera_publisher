from glob import glob
from setuptools import setup

package_name = 'cv_basics'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/config', glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sergei',
    maintainer_email='msghub@hotmail.com',
    description='TODO: Package description',
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'img_publisher_gs = cv_basics.camera_gs_pub:main',
            'img_publisher_raw = cv_basics.webcam_pub_raw:main',
            'img_publisher = cv_basics.webcam_pub:main',
            'fake_camera_info_node = cv_basics.fake_camera_info_node:main',
        ],
    },
)
