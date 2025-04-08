from setuptools import setup, find_packages

setup(
    name='scxmlviz',
    version='0.1.0',
    description='SCXML visualization library for Jupyter and Python scripts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dat Nguyen',
    author_email='thanhdat19022001@gmail.com',
    url='https://github.com/thanhdat1902/scxmlviz',  # optional
    keywords="scxml, AI, event-based",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'scxmlviz': ['static/*.js']
    },
    python_requires='>=3.6',
    install_requires=['IPython'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Jupyter',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)