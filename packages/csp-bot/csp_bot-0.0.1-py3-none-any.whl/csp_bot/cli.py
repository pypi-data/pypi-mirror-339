import logging
import os
import os.path
from pathlib import Path
from pprint import pprint
from typing import List, Optional

import csp_gateway
import hydra
from ccflow import ModelRegistry, RootModelRegistry
from csp_gateway import Gateway
from hydra import compose, initialize_config_dir

from csp_bot import __version__

log = logging.getLogger(__name__)

__all__ = (
    "load_config",
    "load",
    "run",
)


def _find_parent_config_folder(config_dir: str = "config", config_name: str = "", *, basepath: str = ""):
    folder = Path(basepath).resolve()
    exists = (
        (folder / config_dir).exists()
        if not config_name
        else ((folder / config_dir / f"{config_name}.yml").exists() or (folder / config_dir / f"{config_name}.yaml").exists())
    )
    while not exists:
        folder = folder.parent
        if str(folder) == os.path.abspath(os.sep):
            raise FileNotFoundError(f"Could not find config folder: {config_dir} in folder {basepath}")
        exists = (
            (folder / config_dir).exists()
            if not config_name
            else ((folder / config_dir / f"{config_name}.yml").exists() or (folder / config_dir / f"{config_name}.yaml").exists())
        )

    config_dir = (folder / config_dir).resolve()
    if not config_name:
        return folder.resolve(), config_dir, ""
    elif (folder / config_dir / f"{config_name}.yml").exists():
        return folder.resolve(), config_dir, (folder / config_dir / f"{config_name}.yml").resolve()
    return folder.resolve(), config_dir, (folder / config_dir / f"{config_name}.yaml").resolve()


def load_config(
    config_dir: str = "config",
    config_name: str = "",
    overrides: Optional[List[str]] = None,
    *,
    overwrite: bool = False,
    basepath: str = "",
) -> RootModelRegistry:
    overrides = overrides or []
    with initialize_config_dir(config_dir=str(Path(__file__).resolve().parent), version_base=None):
        if config_dir:
            hydra_folder, config_dir, _ = _find_parent_config_folder(config_dir=config_dir, config_name=config_name, basepath=basepath or os.getcwd())

            cfg = compose(config_name="conf", overrides=[], return_hydra_config=True)
            searchpaths = cfg["hydra"]["searchpath"]
            searchpaths.extend([hydra_folder, config_dir])
            if config_name:
                overrides = [f"+config={config_name}", *overrides.copy(), f"hydra.searchpath=[{','.join(searchpaths)}]"]
            else:
                overrides = [*overrides.copy(), f"hydra.searchpath=[{','.join(searchpaths)}]"]

        cfg = compose(config_name="conf", overrides=overrides)

    registry = ModelRegistry.root()
    registry.load_config(cfg, overwrite=overwrite)
    return registry


def load(cfg):
    log.info("Loading csp-bot config...")
    registry = ModelRegistry.root()
    registry.load_config(cfg=cfg, overwrite=True)
    return registry["gateway"]


def run(cfg):
    gateway: Gateway = load(cfg)
    log.info(f"Starting csp_gateway version {csp_gateway.__version__}")
    log.info(f"Starting csp_bot version {__version__}")
    kwargs = cfg["start"]
    if kwargs:  # i.e. start=False override on command line
        log.info(f"Starting gateway with arguments: {kwargs}")
        gateway.start(**kwargs)
    else:
        pprint(gateway.model_dump(by_alias=True))


@hydra.main(config_path="config", config_name="conf", version_base=None)
def main(cfg):
    run(cfg)


if __name__ == "__main__":
    main()
