from dagster._core.libraries import DagsterLibraryRegistry

from dagster_modal.resources import ModalClient as ModalClient

__version__ = "0.0.3"

DagsterLibraryRegistry.register("dagster-modal", __version__)
