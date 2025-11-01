from setuptools import setup

package_name = 'dp_depth_preproc'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/depth_preproc.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Manuel Junior',
    maintainer_email='manueljunior14.mj@gmail.com',
    description='Depth preprocessing node for DP-NeTSDF.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'depth_preproc_node = dp_depth_preproc.node_depth_preproc:main',
        ],
    },
)
