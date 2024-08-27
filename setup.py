from setuptools import setup, find_packages

setup(
    name="sensor",
    version="0.0.0",
    author="Judi Rispah",
    author_email="judi.rispah.123@gmail.com",
    packages=find_packages()
)

#It is helpful for considering sensor as local package
#for runing requirements.txt
#asa soon as i run requirementfile when it reaches the bottom -e. it looks for setup.py and runs it ehich instals sensor as my local package
#if not installed, the local package while importing it shows error (import sensor.components.data_ingestion)
