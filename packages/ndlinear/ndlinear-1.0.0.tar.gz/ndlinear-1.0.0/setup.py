from setuptools import setup, find_packages

setup(
    name='ndlinear',
    version='1.0.0',
    author='Alex Reneau, Jerry Yao-Chieh Hu, Zhongfang Zhuang, Ting-Chun Liu',
    description='NdLinear: A multi-dimensional linear transformation layer.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ensemble-core/NdLinear',
    packages=find_packages(),
    install_requires=[
        'torch>=2.3.0',
        'numpy>=1.24.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)