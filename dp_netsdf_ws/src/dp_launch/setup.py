from setuptools import setup

package_name = 'dp_launch'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/dp_netsdf.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Manuel Junior',
    maintainer_email='manueljunior14.mj@gmail.com',
    description='Launch files for DP-NeTSDF stack.',
    license='MIT',
    entry_points={
        'console_scripts': [],
    },
)
