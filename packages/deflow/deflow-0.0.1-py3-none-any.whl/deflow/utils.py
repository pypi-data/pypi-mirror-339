from pathlib import Path
from typing import Any

from ddeutil.io import YamlEnvFl


def get_process(name: str, path: Path) -> dict[str, Any]:
    """Get Process instance from an input name and path values.

    :param name: (str)
    :param path: (Path)

    :rtype: dict[str, Any]
    """
    for file in path.rglob("*"):
        if file.is_file() and file.stem == name:
            if file.suffix in (".yml", ".yaml"):
                data = YamlEnvFl(path=file).read()
                return {
                    "name": name,
                    "group_name": file.parent.name,
                    "stream_name": file.parent.parent.name,
                    **data,
                }
            else:
                raise NotImplementedError(
                    f"Get process file: {file.name} does not support for "
                    f"type: {file.suffix}."
                )
    raise FileNotFoundError(f"{path}/**/{name}.yml")
