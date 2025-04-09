from setuptools import find_packages, setup

setup(
    name='pymathisrte', 
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyarrow',
        'dotenv',
        'pandas'
    ],
    author='Tatien Dubreuil',  
    author_email='tatien.dubreuil@gmail.com',
    description='A library to have access to MATHIS',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',

)