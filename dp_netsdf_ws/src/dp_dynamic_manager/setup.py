from setuptools import setup

package_name = 'dp_dynamic_manager'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/dynamic_manager.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Manuel Junior',
    maintainer_email='manueljunior14.mj@gmail.com',
    description='Dynamic instance management node for DP-NeTSDF.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'dynamic_manager_node = dp_dynamic_manager.node_dynamic_manager:main',
        ],
    },
)
