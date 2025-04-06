from setuptools import setup, find_packages

setup(
    name='brainnet-graph',
    version='0.1.1',
    description='Graph construction from BOLD signal time series',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Songlin Zhao',
    author_email='your_email@example.com',  # You can put a dummy one
    url='https://github.com/yourname/brainnet-graph',  # Optional
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'pandas',
        'torch',
        'torch-geometric',
        'scikit-learn',
        'tqdm',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'construct-graph=brainnet_graph.construction:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
