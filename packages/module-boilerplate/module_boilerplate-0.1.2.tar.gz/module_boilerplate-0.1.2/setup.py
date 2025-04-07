from setuptools import setup, find_packages

setup(
    name='module_boilerplate',
    version='0.1.2', 
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/SoyVitouPro/python-modules-boilerplate',  # Optional
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
