
import json
from pathlib import Path

from battkit.logging_config import logger
from battkit.dataset import Dataset

# Hides non-specified functions from auto-import
__all__ = [
    "create_dataset", "load_dataset"
]


def create_dataset(name:str, dir_storage:Path, overwriting_existing:bool=False) -> Dataset:
    """Creates a new Dataset instance

    Args:
        name (str): Provide a name for the dataset
        dir_storage (Path): Provide a folder for where this dataset should be stored. 
        overwriting_existing (bool, optional): Whether to override an existing dataset with the same name at the provided directory. Defaults to False.

    Returns:
        Dataset: A new Dataset instance.
    """
    return Dataset(name=name, dir_storage=dir_storage, overwrite_existing=overwriting_existing)

def load_dataset(dir_dataset:Path) -> Dataset:
    """Loads an existing Dataset instance

    Args:
        dir_dataset (Path): Head directory of the stored Dataset instance.

    Returns:
        Dataset: _description_
    """

    if not dir_dataset.is_dir():
        logger.error(f"Path is not a directory: {dir_dataset}")
        raise TypeError(f"The provided path is not a directory: {dir_dataset}")
    file_config = dir_dataset.joinpath("config.json")
    if not file_config.exists():
        logger.error(f"Dataset does not contain a config.json file.")
        raise FileNotFoundError("Could not find a config.json file in this directory.")

    with open(file_config, "r") as f:
        config_data = json.load(f)
        name = config_data['name']

    return Dataset(name=name, dir_storage=dir_dataset.parent)
