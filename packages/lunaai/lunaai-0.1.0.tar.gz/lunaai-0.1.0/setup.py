# setup.py
from setuptools import setup, find_packages

setup(
    name='lunaai',
    version='0.1.0',
    author='Joydeep Dutta',
    author_email='joydeep.development.cse@gmail.com',
    description='A retrieval-based QnA and code generation chatbot using sentence-transformer embeddings.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'gdown',
        'numpy',
        'pandas',
        'sentence-transformers',
        'scikit-learn',
        'nltk',
        'rapidfuzz'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'lunaai=lunaai.main:main',
        ]
    },
)

