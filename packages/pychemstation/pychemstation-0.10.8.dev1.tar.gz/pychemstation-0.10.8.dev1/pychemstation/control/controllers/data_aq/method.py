from __future__ import annotations

import os
import time
import warnings
from typing import List, Optional, Union, Dict, Set

from result import Err, Ok, Result

from ....analysis.process_report import AgilentReport, ReportType
from ....control.controllers import CommunicationController
from pychemstation.analysis.chromatogram import (
    TIME_FORMAT,
    AgilentChannelChromatogramData,
    AgilentHPLCChromatogram,
)
from ....utils.abc_tables.run import RunController
from ....utils.macro import Command
from ....utils.method_types import (
    HPLCMethodParams,
    MethodDetails,
    Param,
    PType,
    TimeTableEntry,
)
from ....utils.table_types import RegisterFlag, Table, TableOperation, T
from ..devices.injector import InjectorController


class MethodController(RunController):
    """Class containing method related logic."""

    def __init__(
        self,
        controller: Optional[CommunicationController],
        src: Optional[str],
        data_dirs: Optional[List[str]],
        table: Table,
        offline: bool,
        injector_controller: InjectorController,
    ):
        self.injector_controller = injector_controller
        self.data_files: List[str] = []
        super().__init__(
            controller=controller,
            src=src,
            data_dirs=data_dirs,
            table=table,
            offline=offline,
        )

    def get_current_method_name(self) -> str:
        time.sleep(2)
        self.send(Command.GET_METHOD_CMD)
        time.sleep(2)
        res = self.receive()
        if res.is_ok():
            return res.ok_value.string_response
        return "ERROR"

    def get_method_params(self) -> HPLCMethodParams:
        if self.controller:
            return HPLCMethodParams(
                organic_modifier=self.controller.get_num_val(
                    cmd=TableOperation.GET_OBJ_HDR_VAL.value.format(
                        register=self.table_locator.register,
                        register_flag=RegisterFlag.SOLVENT_B_COMPOSITION,
                    )
                ),
                flow=self.controller.get_num_val(
                    cmd=TableOperation.GET_OBJ_HDR_VAL.value.format(
                        register=self.table_locator.register,
                        register_flag=RegisterFlag.FLOW,
                    )
                ),
            )
        raise ValueError("Communication controller is offline!")

    def get_row(self, row: int) -> TimeTableEntry:
        flow = None
        om = None

        try:
            flow = self.get_num(row, RegisterFlag.TIMETABLE_FLOW)
        except RuntimeError:
            pass
        try:
            om = self.get_num(row, RegisterFlag.TIMETABLE_SOLVENT_B_COMPOSITION)
        except RuntimeError:
            pass

        if om is None and flow is None:
            raise ValueError("Both flow and organic modifier is None")

        return TimeTableEntry(
            start_time=self.get_num(row, RegisterFlag.TIME),
            organic_modifer=om,
            flow=flow,
        )

    def get_timetable(self, rows: int):
        uncoalesced_timetable_rows = [self.get_row(r + 1) for r in range(rows)]
        timetable_rows: Dict[str, TimeTableEntry] = {}
        for row in uncoalesced_timetable_rows:
            time_key = str(row.start_time)
            if time_key not in timetable_rows.keys():
                timetable_rows[time_key] = TimeTableEntry(
                    start_time=row.start_time,
                    flow=row.flow,
                    organic_modifer=row.organic_modifer,
                )
            else:
                if row.flow:
                    timetable_rows[time_key].flow = row.flow
                if row.organic_modifer:
                    timetable_rows[time_key].organic_modifer = row.organic_modifer
        entries = list(timetable_rows.values())
        entries.sort(key=lambda e: e.start_time)
        return entries

    def load(self) -> MethodDetails:
        rows = self.get_num_rows()
        if rows.is_ok():
            method_name = self.get_method_name()
            timetable_rows = self.get_timetable(int(rows.ok_value.num_response))
            params = self.get_method_params()
            stop_time = self.get_stop_time()
            post_time = self.get_post_time()
            self.table_state = MethodDetails(
                name=method_name,
                timetable=timetable_rows,
                stop_time=stop_time,
                post_time=post_time,
                params=params,
            )
            return self.table_state
        else:
            raise RuntimeError(rows.err_value)

    def get_method_name(self):
        self.send(Command.GET_METHOD_CMD)
        res = self.receive()
        method_name = res.ok_value.string_response
        return method_name

    def get_post_time(self) -> Union[int, float]:
        if self.controller:
            return self.controller.get_num_val(
                cmd=TableOperation.GET_OBJ_HDR_VAL.value.format(
                    register=self.table_locator.register,
                    register_flag=RegisterFlag.POST_TIME,
                )
            )
        raise ValueError("Communication controller is not online!")

    def get_stop_time(self) -> Union[int, float]:
        if self.controller:
            return self.controller.get_num_val(
                cmd=TableOperation.GET_OBJ_HDR_VAL.value.format(
                    register=self.table_locator.register,
                    register_flag=RegisterFlag.MAX_TIME,
                )
            )
        raise ValueError("Communication controller is not online!")

    def get_total_runtime(self) -> Union[int, float]:
        """Returns total method runtime in minutes."""
        return self.get_post_time() + self.get_stop_time()

    def current_method(self, method_name: str):
        """
        Checks if a given method is already loaded into Chemstation. Method name does not need the ".M" extension.

        :param method_name: a Chemstation method
        :return: True if method is already loaded
        """
        self.send(Command.GET_METHOD_CMD)
        parsed_response = self.receive()
        return method_name in parsed_response

    def switch(self, method_name: str, alt_method_dir: Optional[str] = None):
        """
        Allows the user to switch between pre-programmed methods. No need to append '.M'
        to the end of the method name. For example. for the method named 'General-Poroshell.M',
        only 'General-Poroshell' is needed.

        :param method_name: any available method in Chemstation method directory
        :param alt_method_dir: directory where the method resides
        :raise IndexError: Response did not have expected format. Try again.
        :raise AssertionError: The desired method is not selected. Try again.
        """
        method_dir = self.src if not alt_method_dir else alt_method_dir
        self.send(
            Command.SWITCH_METHOD_CMD_SPECIFIC.value.format(
                method_dir=method_dir, method_name=method_name
            )
        )

        time.sleep(2)
        self.send(Command.GET_METHOD_CMD)
        time.sleep(2)
        res = self.receive()
        if res.is_ok():
            parsed_response = res.ok_value.string_response
            assert parsed_response == f"{method_name}.M", "Switching Methods failed."
        self.table_state = None

    def edit(self, updated_method: MethodDetails, save: bool):
        """Updated the currently loaded method in ChemStation with provided values.

        :param updated_method: the method with updated values, to be sent to Chemstation to modify the currently loaded method.
        :param save: if false only modifies the method, otherwise saves to disk
        """
        self.table_state = updated_method
        # Method settings required for all runs
        self.update_method_params(
            new_flow=updated_method.params.flow,
            new_initial_om=updated_method.params.organic_modifier,
            new_stop_time=updated_method.stop_time,
            new_post_time=updated_method.post_time,
        )
        self.edit_method_timetable(updated_method.timetable)

        if save:
            self.send(
                Command.SAVE_METHOD_CMD.value.format(
                    commit_msg=f"saved method at {str(time.time())}"
                )
            )

    def edit_initial_om(self, new_om: Union[int, float]):
        initial_organic_modifier: Param = Param(
            val=new_om,
            chemstation_key=RegisterFlag.SOLVENT_B_COMPOSITION,
            ptype=PType.NUM,
        )
        self._update_param(initial_organic_modifier)

    def edit_flow(self, new_flow: Union[int, float]):
        flow: Param = Param(
            val=new_flow, chemstation_key=RegisterFlag.FLOW, ptype=PType.NUM
        )
        self._update_param(flow)

    def edit_stop_time(self, new_stop_time: Union[int, float]):
        stop_time: Param = Param(
            val=new_stop_time,
            chemstation_key=RegisterFlag.MAX_TIME,
            ptype=PType.NUM,
        )
        self._update_param(
            Param(
                val="Set", chemstation_key=RegisterFlag.STOPTIME_MODE, ptype=PType.STR
            )
        )
        self._update_param(stop_time)

    def edit_post_time(self, new_post_time: Union[int, float]):
        post_time: Param = Param(
            val=new_post_time,
            chemstation_key=RegisterFlag.POST_TIME,
            ptype=PType.NUM,
        )
        self._update_param(
            Param(val="Set", chemstation_key=RegisterFlag.POSTIME_MODE, ptype=PType.STR)
        )
        self._update_param(post_time)

    def update_method_params(
        self,
        new_flow: Union[int, float],
        new_initial_om: Union[int, float],
        new_stop_time: Union[int, float] | None,
        new_post_time: Union[int, float] | None,
    ):
        self.delete_table()
        self.edit_initial_om(new_initial_om)
        self.edit_flow(new_flow)
        if new_stop_time:
            self.edit_stop_time(new_stop_time)
        else:
            self._update_param(
                Param(
                    val="Off",
                    chemstation_key=RegisterFlag.STOPTIME_MODE,
                    ptype=PType.STR,
                )
            )
        if new_post_time:
            self.edit_post_time(new_post_time)
        else:
            self._update_param(
                Param(
                    val="Off",
                    chemstation_key=RegisterFlag.POSTIME_MODE,
                    ptype=PType.STR,
                )
            )

    def _update_param(self, method_param: Param):
        """Change a method parameter, changes what is visibly seen in Chemstation GUI.
         (changes the first row in the timetable)

        :param method_param: a parameter to update for currently loaded method.
        """
        register = self.table_locator.register
        setting_command = (
            TableOperation.UPDATE_OBJ_HDR_VAL
            if method_param.ptype == PType.NUM
            else TableOperation.UPDATE_OBJ_HDR_TEXT
        )
        if isinstance(method_param.chemstation_key, list):
            for register_flag in method_param.chemstation_key:
                self.send(
                    setting_command.value.format(
                        register=register,
                        register_flag=register_flag,
                        val=method_param.val,
                    )
                )
        else:
            self.send(
                setting_command.value.format(
                    register=register,
                    register_flag=method_param.chemstation_key,
                    val=method_param.val,
                )
            )
        time.sleep(2)
        self.download()

    def download(self):
        self.send("Sleep 1")
        self.sleepy_send("DownloadRCMethod PMP1")
        self.send("Sleep 1")

    def _edit_row(self, row: TimeTableEntry, first_row: bool = False):
        if first_row:
            if row.organic_modifer:
                self.add_row()
                self.add_new_col_text(
                    col_name=RegisterFlag.FUNCTION,
                    val=RegisterFlag.SOLVENT_COMPOSITION.value,
                )
                self.add_new_col_num(col_name=RegisterFlag.TIME, val=row.start_time)
                self.add_new_col_num(
                    col_name=RegisterFlag.TIMETABLE_SOLVENT_B_COMPOSITION,
                    val=row.organic_modifer,
                )
            if row.flow:
                self.add_row()
                self.get_num_rows()
                self._edit_row_text(
                    col_name=RegisterFlag.FUNCTION, val=RegisterFlag.FLOW.value
                )
                self.add_new_col_num(col_name=RegisterFlag.TIMETABLE_FLOW, val=row.flow)
                self._edit_row_num(col_name=RegisterFlag.TIMETABLE_FLOW, val=row.flow)
            self.download()
        else:
            if row.organic_modifer:
                self.add_row()
                self.get_num_rows()
                self._edit_row_text(
                    col_name=RegisterFlag.FUNCTION,
                    val=RegisterFlag.SOLVENT_COMPOSITION.value,
                )
                self._edit_row_num(col_name=RegisterFlag.TIME, val=row.start_time)
                self._edit_row_num(
                    col_name=RegisterFlag.TIMETABLE_SOLVENT_B_COMPOSITION,
                    val=row.organic_modifer,
                )
                self.download()
            if row.flow:
                self.add_row()
                self.get_num_rows()
                self._edit_row_text(
                    col_name=RegisterFlag.FUNCTION, val=RegisterFlag.FLOW.value
                )
                self._edit_row_num(col_name=RegisterFlag.TIMETABLE_FLOW, val=row.flow)
                self._edit_row_num(col_name=RegisterFlag.TIME, val=row.start_time)
                self.download()

    def edit_method_timetable(self, timetable_rows: List[TimeTableEntry]):
        self.get_num_rows()
        self.delete_table()
        res = self.get_num_rows()
        while not res.is_err():
            self.delete_table()
            res = self.get_num_rows()

        self.new_table()
        self.get_num_rows()

        for i, row in enumerate(timetable_rows):
            self._edit_row(row=row, first_row=i == 0)

    def stop(self):
        """
        Stops the method run. A dialog window will pop up and manual intervention may be required.
        """
        self.send(Command.STOP_METHOD_CMD)

    def run(
        self,
        experiment_name: str,
        add_timestamp: bool = True,
        stall_while_running: bool = True,
    ):
        """
        :param experiment_name: Name of the experiment
        :param stall_while_running: whether to stall or immediately return
        :param add_timestamp: if should add timestamp to experiment name
        """
        hplc_is_running = False
        tries = 0
        while tries < 10 and not hplc_is_running:
            timestamp = time.strftime(TIME_FORMAT)
            self.send(
                Command.RUN_METHOD_CMD.value.format(
                    data_dir=self.data_dirs[0],
                    experiment_name=f"{experiment_name}_{timestamp}"
                    if add_timestamp
                    else experiment_name,
                )
            )

            hplc_is_running = self.check_hplc_is_running()
            tries += 1

        data_dir, data_file = self.get_current_run_data_dir_file()
        if not hplc_is_running:
            raise RuntimeError("Method failed to start.")

        self.data_files.append(os.path.join(os.path.normpath(data_dir), data_file))
        self.timeout = (self.get_total_runtime()) * 60

        if stall_while_running:
            run_completed = self.check_hplc_done_running()
            if run_completed.is_ok():
                self.data_files[-1] = run_completed.ok_value
            else:
                warnings.warn(run_completed.err_value)
        else:
            folder = self._fuzzy_match_most_recent_folder(self.data_files[-1], None)
            i = 0
            while folder.is_err() and i < 10:
                folder = self._fuzzy_match_most_recent_folder(self.data_files[-1], None)
                i += 1
            if folder.is_ok():
                self.data_files[-1] = folder.ok_value
            else:
                warning = f"Data folder {self.data_files[-1]} may not exist, returning and will check again after run is done."
                warnings.warn(warning)

    def _fuzzy_match_most_recent_folder(
        self, most_recent_folder: T, child_dirs: Optional[Set[str]]
    ) -> Result[str, str]:
        if isinstance(most_recent_folder, str) or isinstance(most_recent_folder, bytes):
            if os.path.exists(most_recent_folder):
                return Ok(most_recent_folder)
            return Err("Folder not found!")
        raise ValueError("Folder is not a str or byte type.")

    def get_data(
        self, custom_path: Optional[str] = None
    ) -> AgilentChannelChromatogramData:
        custom_path = custom_path if custom_path else self.data_files[-1]
        self.get_spectrum_at_channels(custom_path)
        return AgilentChannelChromatogramData.from_dict(self.spectra)

    def get_data_uv(
        self, custom_path: Optional[str] = None
    ) -> dict[int, AgilentHPLCChromatogram]:
        custom_path = custom_path if custom_path else self.data_files[-1]
        self.get_uv_spectrum(custom_path)
        return self.uv

    def get_report(
        self,
        custom_path: Optional[str] = None,
        report_type: ReportType = ReportType.TXT,
    ) -> List[AgilentReport]:
        custom_path = self.data_files[-1] if not custom_path else custom_path
        metd_report = self.get_report_details(custom_path, report_type)
        chrom_data: List[AgilentHPLCChromatogram] = list(
            self.get_data(custom_path).__dict__.values()
        )
        for i, signal in enumerate(metd_report.signals):
            possible_data = chrom_data[i]
            if len(possible_data.x) > 0:
                signal.data = possible_data
        return [metd_report]
