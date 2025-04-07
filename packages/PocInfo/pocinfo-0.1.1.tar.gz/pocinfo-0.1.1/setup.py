from setuptools import setup, find_packages

setup(
    name="PocInfo",
    version="0.1.1",
    description="Utiliser pour les self bots python, integre des functions pour return ses infos de compte.",
    author="Distinguer",
    url="https://github.com/Uwu-Kagami",
    packages=find_packages(),
    long_description= "Utiliser pour les self bots python, integre des functions pour return ses infos de compte.",
    install_requires=[ 
        'pypiwin32',
        'pycryptodome',
        'requests',  
    ],
    long_description_content_type="text/markdown",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
