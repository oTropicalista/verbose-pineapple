![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg)
# aurpy

## DESCRIPTION
Tool for searching and installing packages from Arch User Repository directly from the terminal.

## REQUIREMENTS
os
time
pycurl
argparse
subprocess
BytesIO
BeautifulSoup

## Usage
Search packages
```
$ python aur.py name_package
```
Install packages
```
$ python aur.py -S name_package
```