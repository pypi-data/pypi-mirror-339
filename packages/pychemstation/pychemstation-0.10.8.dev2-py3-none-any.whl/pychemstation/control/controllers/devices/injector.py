from __future__ import annotations

from ....control.controllers import CommunicationController
from ....utils.abc_tables.device import DeviceController
from ....utils.injector_types import (
    Draw,
    Inject,
    InjectorTable,
    Mode,
    Remote,
    RemoteCommand,
    SourceType,
    Wait,
    DrawDefault,
    DrawDefaultVolume,
    DrawDefaultLocation,
)
from ....utils.macro import Response
from ....utils.table_types import RegisterFlag, Table
from ....utils.tray_types import Tray, FiftyFourVialPlate, VialBar, LocationPlus


class InjectorController(DeviceController):
    def __init__(
        self, controller: CommunicationController, table: Table, offline: bool
    ):
        super().__init__(controller, table, offline)

    def try_vial_location(self, val: str) -> Tray:
        try:
            return FiftyFourVialPlate.from_str(val)
        except Exception:
            try:
                return VialBar(int(val))
            except Exception:
                raise ValueError("Location could not be identified.")

    def get_row(
        self, row: int
    ) -> (
        Draw
        | DrawDefaultVolume
        | Inject
        | Wait
        | DrawDefault
        | DrawDefaultLocation
        | Remote
    ):
        def return_location_plus() -> Tray:
            unit = self.get_num(row, RegisterFlag.DRAW_LOCATION_UNIT)
            tray = self.get_num(row, RegisterFlag.DRAW_LOCATION_TRAY)
            row_ = self.get_num(row, RegisterFlag.DRAW_LOCATION_ROW)
            col = self.get_num(row, RegisterFlag.DRAW_LOCATION_COLUMN)
            return LocationPlus(int(unit), int(tray), int(row_), int(col))

        function = self.get_text(row, RegisterFlag.FUNCTION)
        if function == "Wait":
            return Wait(duration=self.get_num(row, RegisterFlag.TIME))
        elif function == "Inject":
            return Inject()
        elif function == "Draw":
            is_source = SourceType(self.get_text(row, RegisterFlag.DRAW_SOURCE))
            is_volume = Mode(self.get_text(row, RegisterFlag.DRAW_VOLUME))
            if is_volume is not Mode.SET:
                if is_source == SourceType.DEFAULT:
                    return DrawDefault()
                elif is_source is SourceType.SPECIFIC_LOCATION:
                    return DrawDefaultVolume(location=return_location_plus())
                elif is_source is SourceType.LOCATION:
                    return DrawDefaultVolume(
                        location=self.try_vial_location(
                            self.get_text(row, RegisterFlag.DRAW_LOCATION)
                        )
                    )
            else:
                vol = self.get_num(row, RegisterFlag.DRAW_VOLUME_VALUE)
                if is_source == SourceType.DEFAULT:
                    return DrawDefaultLocation(amount=vol)
                elif is_source is SourceType.SPECIFIC_LOCATION:
                    return Draw(amount=vol, location=return_location_plus())
                elif is_source is SourceType.LOCATION:
                    return Draw(
                        amount=vol,
                        location=self.try_vial_location(
                            self.get_text(row, RegisterFlag.DRAW_LOCATION)
                        ),
                    )
        elif function == "Remote":
            return Remote(
                command=RemoteCommand(self.get_text(row, RegisterFlag.REMOTE)),
                duration=int(self.get_num(row, RegisterFlag.REMOTE_DUR)),
            )
        raise ValueError("No valid function found.")

    def load(self) -> InjectorTable | None:
        rows = self.get_num_rows()
        if rows.is_ok():
            row_response = rows.value
            if isinstance(row_response, Response):
                return InjectorTable(
                    functions=[
                        self.get_row(i + 1)
                        for i in range(int(row_response.num_response))
                    ]
                )
        raise ValueError("Couldn't read injector table rows.")
