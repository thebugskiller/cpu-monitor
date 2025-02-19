from setuptools import setup

setup(
    name='cpu-monitor',
    version='0.1',
    py_modules=['main', 'monitor', 'util', 'service'],
    install_requires=[
        'tabulate>=0.9.0',
        'colorama>=0.4.6',
        'requests>=2.32.3',
        'click>=8.1.7',
        'psutil>=5.9.6'
    ],
    entry_points={
        'console_scripts': [
            'cpu-monitor=main:main'
        ]
    }
)
