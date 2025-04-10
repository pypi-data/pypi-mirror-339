from setuptools import setup, find_packages

setup(
    name='PythonSoundPlayerX',
    version='0.1',
    packages=find_packages(),
    install_requires=['pygame'],
    author='Ruzgar',
    description='Python 3.13 uyumlu sessiz mp3/wav oynatici kutuphane',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ruzgar/PythonSoundPlayerX',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
