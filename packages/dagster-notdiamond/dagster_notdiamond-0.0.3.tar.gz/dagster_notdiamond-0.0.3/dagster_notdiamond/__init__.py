from dagster._core.libraries import DagsterLibraryRegistry

from dagster_notdiamond.resources import (
    NotDiamondResource as NotDiamondResource,
)

__version__ = "0.0.3"

DagsterLibraryRegistry.register("dagster-notdiamond", __version__)
