from setuptools import setup, find_packages

setup(
    name='rdlab-dataset',
    version='0.0.2', 
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='soyvitou',
    author_email='soyvitoupro@gmail.com',
    url='https://github.com/SoyVitouPro/rdlab-dataset',  # Optional
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
