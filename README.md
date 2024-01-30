## Package-Sieve 
No BS, but modules :sparkles:. Collector of absolute 3rd party packages from existing projects with relevant versions. 

### Background
This project aims to generate `requirements.txt` file for existing repositories where you have an old file which is filled with dependencies of dependencies :cyclone: :dizzy_face:. 

### Function
Wall-E uses `ast` module of python to parse nodes of any python script. Once the modules are retrieved, `pkg_resources` helps to find the right project name :detective: and version of the application installed. 

### Install

```console
pip3 install package-sieve 
```

### Usage 
```console
package-sieve --project_folder /absolute/path/to/folder --ignore venv,__pycache__,__init__.py
```
`--project_folder` - this is a mandatory parameter which mentions the root of the directory,  defaults to the current working directory.

`--ignore` - Mention the folders you want to ignore to create the requirements, optional parameter. By default this holds all the folder patterns added in your `.gitignore` file, if exists.

> NOTE:  
If you get this error `ModuleNotFoundError: No module named 'pkg_resources'`
Just run `pip3 install setuptools` 
