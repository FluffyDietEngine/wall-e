from ast import parse
from typing import Any
from ast import NodeVisitor
from pathlib import Path
from argparse import ArgumentParser
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from pkg_resources import get_distribution  # type: ignore

from pkg_resources import DistributionNotFound

# Derived out of Python .gitignore file from https://github.com/github/gitignore/blob/main/Python.gitignore
IGNORE_DIRECTORIES = [
    "__pycache__",
    "build",
    "develop-eggs",
    "dist",
    "downloads",
    "eggs",
    ".eggs",
    "lib",
    "lib64",
    "parts",
    "sdist",
    "var",
    "wheels",
    "sharepython-wheels",
    "*.egg-info",
    "htmlcov",
    ".tox",
    ".nox",
    ".hypothesis",
    ".pytest_cache",
    "cover",
    "instance",
    "docs_build",
    ".pybuilder",
    "target",
    "profile_default",
    "__pypackages__",
    "env",
    "venv",
    "ENV",
    "env.bak",
    "venv.bak",
    ".mypy_cache",
    ".pyre",
    ".pytype",
    "cython_debug",
]


class ImportCollector(NodeVisitor):
    """
    Extended `NodeVisitor` class to collect imported nodes
    in a given python file.

    `visit_Import` and `visit_ImportFrom` has been overridden
    to check whether the module is standard or third party
    based on the installation location

    """

    def __init__(self):
        self.imports = set()

    def visit_Import(self, node):
        for alias in node.names:
            try:
                if "site-packages" in __import__(alias.name).__file__:
                    self.imports.add(alias.name)
            except ModuleNotFoundError:
                self.imports.add(alias.name)
            except (AttributeError, TypeError):
                pass
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            try:
                if "site-packages" in __import__(module).__file__:
                    self.imports.add(module if module else alias.name)
            except ModuleNotFoundError:
                self.imports.add(module if module else alias.name)
            except (AttributeError, TypeError):
                pass
        self.generic_visit(node)


def get_modules_from_file(filename: Path) -> set:
    """
    uses `ImportCollector` to analyse and collect third-party modules

    Args:
        filename (str): absolute file path

    Returns:
        set: set of third party module names
    """
    with open(filename, "r") as file:
        node = parse(file.read())
        collector = ImportCollector()
        collector.visit(node)
        return collector.imports


def traverse_directory(
    project_root: str, ignore_directories: list
) -> dict[str, set[str]]:
    """
    Traverse through all files in the given directory,
    ignoring files and folders in ignore_patterns list of relative paths.

    :param base_path: Path of the directory to traverse.
    :param ignore_patterns: List of relative file or folder paths to exclude.
    """

    # third_party_modules: set[str] = set()
    imported_modules: dict[str, set[str]] = {
        "third_party_modules": set(),
        "internal_modules": set(),
    }

    base_path = Path(project_root)

    for item in base_path.rglob("*"):
        if any(
            directory_part in ignore_directories for directory_part in item.parts
        ) or item.suffix not in [".py", ".ipynb"]:
            # this skips any file inside ignore_directories and non-python files
            continue
        else:
            modules = get_modules_from_file(item)
            for module in modules:
                module_name = ""

                # to split module names like "pymysql.cursors"
                if "." in module:
                    module = module.split(".")[0]

                try:
                    package_info = get_distribution(module)
                    module_name = f"{package_info.project_name}=={package_info.version}"
                    imported_modules["third_party_modules"].add(module_name)
                except DistributionNotFound:
                    # modules like bs4, twocaptcha
                    imported_modules["internal_modules"].add(module)

    return imported_modules


def main() -> Any:
    parser = ArgumentParser()
    parser.add_argument(
        "--project_folder", help="Absolute path of the project directory", required=True
    )

    parser.add_argument(
        "--ignore",
        help="Files/Folders to be ignored in comma seperated manner. Eg. venv, __pycache__ etc",
        required=False,
        default=[],
    )

    args = parser.parse_args()

    if args.ignore:
        IGNORE_DIRECTORIES.extend(args.ignore)

    modules = traverse_directory(args.project_folder, IGNORE_DIRECTORIES)

    with open("requirements.txt", "w") as file:
        third_party_modules = modules.get("third_party_modules", [])  # type: ignore
        internal_modules = modules.get("internal_modules", [])  # type: ignore

        if third_party_modules:
            file.write("\n".join(third_party_modules))

        if internal_modules:
            file.write("\n\n# 🚨 Modules to verify 🚨\n\n")
            file.write("\n".join(f"# {module}" for module in internal_modules))


if __name__ == "__main__":
    """
    Known issues:
    1. Modules with different project name and import names are not covered Eg. BeautifulSoup4 @ bs4
    2. Modules which are not used in code will not be covered. Eg. ruff, black
    """
    main()
