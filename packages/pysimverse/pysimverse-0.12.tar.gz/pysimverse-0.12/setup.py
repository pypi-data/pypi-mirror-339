from distutils.core import setup

setup(
    name='pysimverse',
    packages=['pysimverse'],
    version='0.12',
    license='MIT',
    description='Python Computer Vision and Robotics Simulator',
    author='Computer Vision Zone',
    author_email='contact@computervision.zone',
    url='https://github.com/cvzone/pysimverse.git',
    keywords=['ComputerVision', 'Simulator', 'Robotics', 'Drone'],
    install_requires=[
        'pyzmq',
        'opencv-python',
    ],
    python_requires='>=3.7',  # Requires any version >= 3.7
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    package_data={
        'pysimverse': ['simulators/*','simulators/drone/*'],  # Include the files in assets and ui folders
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
    ],
)
