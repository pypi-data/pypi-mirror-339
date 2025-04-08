
from setuptools import setup

setup(
    name='csv_filter_splitter',
    version='0.1.0',
    description='CSV splitter using filter column',
    url='https://github.com/ricardogalindo24/csv-filter-splitter',
    author='Ricardo Galindo',
    author_email='jrichardgali@outlook.com',
    license='BSD 2-clause',
    packages=['csv_splitter'],
    package_dir={"": "src"},
    package_data={"csv_splitter": ["csv_splitter.tcss"]},
    include_package_data=True,
    install_requires=['pandas==2.2.3',
                      'textual==3.0.1',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points = {'console_scripts' : ['csv_splitter = csv_splitter.csv_splitter_interface:launch_app']}
)