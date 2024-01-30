import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
DESCRIPTION = (HERE / "README.md").read_text()

setup(
    name = 'package-sieve',
    version = '0.3.0',
    description = 'Collector of absolute 3rd party packages from existing projects',
    long_description = DESCRIPTION,
    long_description_content_type="text/markdown",
    url = 'https://github.com/FluffyDietEngine/wall-e',
    author = 'Santhosh Solomon',
    author_email = 'solomon.santhosh@gmail.com',
    license = 'Apache License 2.0',
    platforms='any',
    classifiers = [
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
    ],
    packages=["src"],
    include_package_data=True,
    entry_points={
        "console_scripts":[
            "package-sieve=src.wall_e:main",
        ]
    },
    keywords='package-sieve,wall-e,ci,automation,linter,stale-package-remover, developer-tools',
)
