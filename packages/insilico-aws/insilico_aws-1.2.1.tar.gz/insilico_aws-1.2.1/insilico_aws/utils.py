import shutil
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from typing import Any, Optional

try:
    __version__ = version('insilico-aws')
except PackageNotFoundError:
    __version__ = 'dev'


def validate_parameters(schema: list[dict[str, Any]], inputs: Optional[dict[str, Any]]):
    if not inputs:
        return {}
    allowed_names = {k['Name'] for k in schema}
    user_names = {k for k in inputs}
    if unknown_params := allowed_names - user_names:
        raise ValueError(
            f"Params names not supported: "
            f"{', '.join(unknown_params)}; "
            f"allowed: {', '.join(allowed_names)}"
        )
    for k, v in inputs.items():
        for p in schema:
            if p['Name'] == k:
                if not isinstance(v, {  # type: ignore
                    'Integer': int,
                    'Continuous': (float, int),
                    'Categorical': str
                }[p['Type']]):
                    raise ValueError(
                        f"Unsupported {k} param type, "
                        f"expected {p['Type']}, got {type(v).__name__}"
                    )
                break
    return inputs


def load_examples(overwrite: bool = False):
    examples_dir = 'examples'
    return shutil.copytree(
        src=Path(__file__).parent / examples_dir,
        dst=Path.cwd() / examples_dir,
        dirs_exist_ok=overwrite
    )
