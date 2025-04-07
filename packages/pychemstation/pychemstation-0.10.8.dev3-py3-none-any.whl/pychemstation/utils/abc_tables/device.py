from __future__ import annotations

from abc import ABC

from .table import ABCTableController
from ..table_types import Table
from ...control.controllers import CommunicationController


class DeviceController(ABCTableController, ABC):
    """Abstract controller representing tables that contain device information.

    :param controller: controller for sending MACROs
    :param table: contains register keys for accessing table in Chemstation
    :param offline: whether the communication controller is online.
    """

    def __init__(
        self, controller: CommunicationController, table: Table, offline: bool
    ):
        super().__init__(controller=controller, table=table)
        self.offline = offline

    def __new__(cls, *args, **kwargs):
        if cls is ABCTableController:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls)
