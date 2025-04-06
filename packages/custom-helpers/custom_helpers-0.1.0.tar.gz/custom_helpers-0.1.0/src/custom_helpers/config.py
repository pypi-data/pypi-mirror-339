import os
from omegaconf import OmegaConf
from typing import Iterable

def get_config(path: str, root: str | None = None) -> OmegaConf:
    """Get the configuration from the YAML file.
    Set `root_dir` to the directory of the config file.

    :@param path: Path to configuration file (conf.yaml).
    :@param root: Root directory of the project. If None, it will be set to the directory of the config file.
    """
    conf_raw = OmegaConf.load(path)
    conf_raw.root_dir = root or os.path.abspath(os.path.dirname(path))
    conf = OmegaConf.create(OmegaConf.to_yaml(conf_raw, resolve=True))
    return conf
