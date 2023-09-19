from os import path


def directory_path(file: str) -> str:
    return path.dirname(path.realpath(file))
