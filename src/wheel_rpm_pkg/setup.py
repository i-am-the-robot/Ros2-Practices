from setuptools import find_packages, setup

package_name = 'wheel_rpm_pkg'

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
    maintainer='titilola',
    maintainer_email='titilola@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'rpmPublisher = wheel_rpm_pkg.rpmPublisher:main',
        'accSubscriber = wheel_rpm_pkg.accSubscriber:main',
        'publisher = wheel_rpm_pkg.publisher:main',
        'subscriber = wheel_rpm_pkg.subscriber:main',
        'rpm_pub = wheel_rpm_pkg.rpm_pub:main',
        'speed_calc = wheel_rpm_pkg.speed_calc:main',
        ],
    },
)
