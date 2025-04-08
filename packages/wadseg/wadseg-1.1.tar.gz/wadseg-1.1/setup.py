import setuptools

setuptools.setup(
    name='wadseg',  
    version='1.1',   
    author='Feiyu Qu',  
    author_email='qufy66@gmail.com',  
    description='This is a implementation of WADSeg',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    packages=setuptools.find_packages(), 
    classifiers=[                               
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['transformers', 'torch', 'matplotlib', 'matplotlib', 'numpy', 'seaborn', 'spacy' ],  
    url='https://github.com/qufy6/wadseg',  
    python_requires='>=3.6', 
)