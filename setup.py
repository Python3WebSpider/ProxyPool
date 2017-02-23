from setuptools import setup

setup(
    name='proxypool',
    version='1.0.0',
    description='High-performance cross-platform proxy pool',
    long_description='Please go to https://github.com/WiseDoge/ProxyPool',
    author='wisedoge',
    author_email='wisedoge@outlook.com',
    url='https://github.com/WiseDoge/ProxyPool',
    packages=[
        'proxypool'
    ],
    py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'aiohttp',
        'requests',
        'bs4',
        'flask',
        'redis',
        'lxml'
    ],
    entry_points={
        'console_scripts': ['proxypool_run=run:cli']
    },
    license='apache 2.0',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
