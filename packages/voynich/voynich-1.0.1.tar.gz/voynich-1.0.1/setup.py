from setuptools import setup, find_packages

setup(
    name='voynich',  
    version='1.0.1',  
    author='Kal D. Abali', 
    author_email='prince@merlinfinancial.tech',  
    description='The Python SDK for The Voynich Ledger',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/prince-kal/py-voynich',  
    packages=find_packages(),  
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[  
        'aiohttp',  
    ],
    python_requires='>=3.6',  
)
