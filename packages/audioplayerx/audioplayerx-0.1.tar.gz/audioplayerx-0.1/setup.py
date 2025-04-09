from setuptools import setup, find_packages

setup(
    name='audioplayerx',
    version='0.1',
    packages=find_packages(),
    install_requires=['playsound; platform_system=="Windows"'],
    author='Ruzgar',
    description='mp3 ve wav calabilen sade kutuphane',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ruzgar/audioplayerx',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
