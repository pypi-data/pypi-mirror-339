from setuptools import setup, find_packages


setup(
    name='plotly_upset_hd',
    version='0.0.2',
    license='MIT',
    url="https://github.com/pranjalpruthi/plotly-upset-hd",
    author="Pranjal Pruthi",
    author_email="pranjalpruthi@gmail.com",
    maintainer="Pranjal Pruthi",
    maintainer_email="pranjalpruthi@gmail.com",
    description="UpSet intersection visualization utility for Plotly (Python-only) - Fork of plotly-upset by Hasan Shahrier",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'plotly>=5.5.0',
        'numpy>=1.21.6',
        'pandas>=1.3.5',
        'kaleido>=0.2.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
