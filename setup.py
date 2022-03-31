from setuptools import setup, find_packages
 
classifiers = [
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9'
]
 
setup(
  name='goldysmarthouse',
  version='1.0dev2',
  description='A shity python module that allows a Google Assistant device (Google Home, etc) to run code on your computer.', 
  long_description=open('README.txt').read(), 
  url='', 
  project_urls={"Bug Tracker": "https://github.com/THEGOLDENPRO/Goldy-Smart-House/issues"}, 
  author='Dev Goldy', 
  author_email='goldy@novauniverse.net', 
  license='MIT', 
  classifiers=classifiers, 
  keywords=['goldysmarthouse', 'goldy smart house', 'smart goldy house', "google home", "google assistant", "google home client"], 
  packages=find_packages(), 
  install_requires=["requests", "googlecontroller", "librosa"],
  python_requires=">=3.7"
)