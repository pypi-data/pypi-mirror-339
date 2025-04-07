import os
from typing import List, Optional

from ccflow import ModelRegistry, RootModelRegistry
from omegaconf import OmegaConf

# Register a resolver to boolean if an interpolated value is not provided
# This is used to disable modules in the config if an input doesn't exist
OmegaConf.register_new_resolver("is_missing", lambda a, *, _parent_: a not in _parent_)


def load(
    overrides: Optional[List[str]] = None,
    overwrite: bool = False,
    config_dir: Optional[str] = None,
    version_base: Optional[str] = None,
) -> RootModelRegistry:
    """Load the ETL registry.

    :param overrides: List of hydra-style override strings.
        For example, to override the base_path and cds_sql, you could pass:

        overrides=["base_path='/isilon/data01/users/pt10597'", "cds_sql='RESEARCHSQL'"]
    :param overwrite: Whether to over-write existing entries in the registry
    :param config_dir: Equivalent behavior of the command line argument --config-dir, used to point to
        a directory containing user-defined configs.
    :param version_base: See https://hydra.cc/docs/upgrades/version_base/
    :return: The instance of the root model registry, with the configs loaded.
    """

    import hydra

    overrides = overrides or []
    with hydra.initialize_config_dir(version_base=version_base, config_dir=os.path.dirname(__file__)):
        if config_dir is not None:
            # Add config_dir to searchpath overrides (which is what hydra does under the hood)
            # This is a little complicated as we first need to load existing searchpaths
            cfg = hydra.compose(config_name="conf.yaml", return_hydra_config=True, overrides=overrides)
            searchpaths = cfg["hydra"]["searchpath"]
            searchpaths += [config_dir]
            overrides = overrides.copy() + [f"hydra.searchpath=[{','.join(searchpaths)}]"]

        cfg = hydra.compose(config_name="conf.yaml", overrides=overrides)
    r = ModelRegistry.root()
    r.load_config(cfg, overwrite=overwrite)
    return r
