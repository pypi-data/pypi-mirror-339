from setuptools import setup, find_packages  

setup(  
    name='nexum',  
    version='1.0.1',  
    packages=find_packages(),  
    install_requires=[  
        'stem==1.8.2',
        'requests==2.27.0',
        'bs4'
    ],  
    author='Redpiar',  
    author_email='Regeonwix@gmail.com',  
    description='easy using AI, more texting models!',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/RedPiarOfficial/nexumAi',
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
    keywords=[
        'flux',
        'ai',
        'gemini',
        'gpt',
        'completions',
        'grok',
        'diffusion',
        'gpt-4',
        'qwen2',
        'llama3',
        'gpt-4o',
        'gpt-4o-mini',
        'o1-mini',
        'deepseek-r1'
    ],
    python_requires='>=3.9',  
)  