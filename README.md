# Wall-E aka package-sieve
Collector of absolute 3rd party packages from existing projects

![package-sieve](assets/img.jpg)

## Background
This project aims to generate `requirements.txt` file for existing repositories where you have an old file which is filled with dependencies of dependencies. 

## Function
Wall-E uses `ast` module of python to parse nodes of any python script. Once the modules are retrieved, `pkg_resources` helps to find the right project name and version of the application installed. 

## Install

```console
pip3 install package-sieve 
```

## Usage 
```console
package-sieve --project_folder /absolute/path/to/folder --exclude venv,__pycache__,__init__.py
```
> NOTE:  
If you get this error `ModuleNotFoundError: No module named 'pkg_resources'`
Just run `pip3 install setuptools` 
