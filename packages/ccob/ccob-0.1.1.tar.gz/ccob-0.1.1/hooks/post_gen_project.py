#!/usr/bin/env python
import pathlib
import shutil

if __name__ == "__main__":
    if "{{ cookiecutter.create_author_file }}" != "y":
        pathlib.Path("AUTHORS.rst").unlink()
        pathlib.Path("docs", "authors.rst").unlink()

    for website in ["gitee", "gitcode", "github"]:
        if "{{cookiecutter.git_website}}" != website:
            shutil.rmtree(pathlib.Path(f".{website}"), True)

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        pathlib.Path("LICENSE").unlink()
