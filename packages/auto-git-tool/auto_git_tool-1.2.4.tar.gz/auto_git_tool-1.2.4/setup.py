from setuptools import setup, find_packages

setup(
    name="auto-git-tool",
    version="1.2.4",
    packages=find_packages(),
    install_requires=[
        'jst-aicommit',
        'rich',
        
    ],
    entry_points={
        'console_scripts': [
            'autogit=auto_git.cli:aic',  
        ],
    },
    url="https://github.com/Husanjonazamov/auto-git",
    author="Husanjon Azamov",
    author_email="azamovhusanboy@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)