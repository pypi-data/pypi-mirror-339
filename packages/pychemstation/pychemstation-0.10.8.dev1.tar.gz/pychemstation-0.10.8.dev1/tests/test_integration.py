import time
import unittest

from pychemstation.utils.method_types import (
    HPLCMethodParams,
    MethodDetails,
    TimeTableEntry,
)
from pychemstation.utils.sequence_types import (
    InjectionSource,
    SampleType,
    SequenceEntry,
    SequenceTable,
)
from pychemstation.utils.tray_types import FiftyFourVialPlate, Letter, Num, Plate
from tests.constants import (
    DEFAULT_METHOD,
    DEFAULT_SEQUENCE,
    clean_up,
    set_up_utils,
    DEFAULT_METHOD_254,
    DEFAULT_METHOD_242,
)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        num = 254
        self.hplc_controller = set_up_utils(num, offline=False, runs=True)
        self.other_default = DEFAULT_METHOD_242 if num == 242 else DEFAULT_METHOD_254

    def tearDown(self):
        clean_up(self.hplc_controller)

    def test_run_method_many_times(self):
        self.hplc_controller.switch_method(DEFAULT_METHOD)
        rand_method = MethodDetails(
            name=DEFAULT_METHOD,
            params=HPLCMethodParams(organic_modifier=5, flow=0.65),
            timetable=[TimeTableEntry(start_time=0.5, organic_modifer=100, flow=0.65)],
            stop_time=1,
            post_time=0.5,
        )
        self.hplc_controller.edit_method(rand_method, save=True)
        try:
            for _ in range(5):
                self.hplc_controller.run_method(experiment_name="test_experiment")
                chrom = self.hplc_controller.get_last_run_method_data()
                uv = self.hplc_controller.get_last_run_method_data(read_uv=True)
                repos = self.hplc_controller.get_last_run_method_report()
                self.assertEqual(
                    repos.vial_location, FiftyFourVialPlate.from_str("P1-F2")
                )
                self.assertEqual(repos.signals[0].wavelength, 210)
                self.assertIsNotNone(
                    repos.signals[0].data,
                )
                self.assertTrue(210 in uv.keys())
                self.assertTrue(len(chrom.A.x) > 0)
        except Exception as e:
            self.fail(f"Should have not failed: {e}")

    def test_update_method_update_seq_table_run(self):
        try:
            loc = FiftyFourVialPlate(plate=Plate.ONE, letter=Letter.A, num=Num.TWO)
            self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
            seq_table = SequenceTable(
                name=DEFAULT_SEQUENCE,
                rows=[
                    SequenceEntry(
                        vial_location=loc,
                        sample_name="run seq with new method",
                        method=self.other_default,
                        inj_source=InjectionSource.HIP_ALS,
                        inj_vol=0.5,
                        num_inj=1,
                        sample_type=SampleType.SAMPLE,
                    )
                ],
            )
            self.hplc_controller.edit_sequence(seq_table)

            self.hplc_controller.method_controller.switch(DEFAULT_METHOD)
            rand_method = MethodDetails(
                name=DEFAULT_METHOD,
                params=HPLCMethodParams(organic_modifier=5, flow=0.65),
                timetable=[
                    TimeTableEntry(start_time=1, organic_modifer=100, flow=0.65)
                ],
                stop_time=2,
                post_time=1,
            )
            self.hplc_controller.edit_method(rand_method, save=True)
            self.hplc_controller.preprun()
            self.hplc_controller.run_sequence()
            chrom = self.hplc_controller.get_last_run_sequence_data()
            uv = self.hplc_controller.get_last_run_sequence_data(read_uv=True)
            self.assertEqual(len(chrom), 1)
            self.assertEqual(len(uv), 1)
        except Exception:
            self.fail("Failed")

    def test_run_sequence(self):
        try:
            self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
            seq_table = SequenceTable(
                name=DEFAULT_SEQUENCE,
                rows=[
                    SequenceEntry(
                        vial_location=FiftyFourVialPlate(
                            plate=Plate.ONE, letter=Letter.A, num=Num.ONE
                        ),
                        sample_name="P1-A1",
                        data_file="P1-A1",
                        method=DEFAULT_METHOD,
                        inj_source=InjectionSource.HIP_ALS,
                        inj_vol=0.5,
                        num_inj=1,
                        sample_type=SampleType.SAMPLE,
                    ),
                    SequenceEntry(
                        vial_location=FiftyFourVialPlate(
                            plate=Plate.ONE, letter=Letter.A, num=Num.TWO
                        ),
                        sample_name="P1-A2",
                        data_file="P1-A2",
                        method=DEFAULT_METHOD,
                        inj_source=InjectionSource.HIP_ALS,
                        inj_vol=0.5,
                        num_inj=1,
                        sample_type=SampleType.SAMPLE,
                    ),
                    SequenceEntry(
                        vial_location=FiftyFourVialPlate(
                            plate=Plate.ONE, letter=Letter.A, num=Num.THREE
                        ),
                        sample_name="P1-F2",
                        data_file="P1-F2",
                        method=self.other_default,
                        inj_source=InjectionSource.HIP_ALS,
                        inj_vol=0.5,
                        num_inj=1,
                        sample_type=SampleType.SAMPLE,
                    ),
                ],
            )
            self.hplc_controller.edit_sequence(seq_table)
            self.hplc_controller.switch_method(method_name=DEFAULT_METHOD)
            method = MethodDetails(
                name=DEFAULT_METHOD,
                params=HPLCMethodParams(organic_modifier=5, flow=0.65),
                timetable=[
                    TimeTableEntry(start_time=0.50, organic_modifer=100, flow=0.65)
                ],
                stop_time=1,
                post_time=1,
            )
            self.hplc_controller.edit_method(method)
            self.hplc_controller.preprun()
            self.hplc_controller.run_sequence()
            chroms = self.hplc_controller.get_last_run_sequence_data()
            repo = self.hplc_controller.get_last_run_sequence_reports()
            self.assertEqual(len(repo), 3)
            self.assertTrue(len(chroms) == 3)
        except Exception:
            self.fail("Failed")

    def test_run_method_immidiate_return(self):
        self.hplc_controller.switch_method(DEFAULT_METHOD)
        rand_method = MethodDetails(
            name=DEFAULT_METHOD,
            params=HPLCMethodParams(organic_modifier=5, flow=0.65),
            timetable=[TimeTableEntry(start_time=0.5, organic_modifer=100, flow=0.65)],
            stop_time=1,
            post_time=0.5,
        )
        self.hplc_controller.edit_method(rand_method, save=True)
        try:
            for _ in range(5):
                self.hplc_controller.run_method(
                    experiment_name="test_experiment", stall_while_running=False
                )
                time_left, done = self.hplc_controller.check_method_complete()
                while not done:
                    time.sleep(abs(time_left / 2))
                    print(time_left)
                    time_left, done = self.hplc_controller.check_method_complete()
                chrom = self.hplc_controller.get_last_run_method_data()
                uv = self.hplc_controller.get_last_run_method_data(read_uv=True)
                repos = self.hplc_controller.get_last_run_method_report()
                self.assertEqual(
                    repos.vial_location, FiftyFourVialPlate.from_str("P1-A3")
                )
                self.assertEqual(repos.signals[0].wavelength, 210)
                self.assertTrue(210 in uv.keys())
                self.assertTrue(len(chrom.A.x) > 0)
        except Exception as e:
            self.fail(f"Should have not failed: {e}")

    def test_update_method_update_seq_table_run_immidiate_return(self):
        try:
            loc1 = FiftyFourVialPlate.from_str("P1-A2")
            loc2 = FiftyFourVialPlate.from_str("P1-F2")
            self.assertEqual(
                loc1, FiftyFourVialPlate(plate=Plate.ONE, letter=Letter.A, num=Num.TWO)
            )
            self.assertEqual(
                loc2, FiftyFourVialPlate(plate=Plate.ONE, letter=Letter.F, num=Num.TWO)
            )
            self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
            seq_table = SequenceTable(
                name=DEFAULT_SEQUENCE,
                rows=[
                    SequenceEntry(
                        vial_location=loc1,
                        sample_name="run seq with new method",
                        method=DEFAULT_METHOD,
                        inj_source=InjectionSource.HIP_ALS,
                        inj_vol=0.5,
                        num_inj=1,
                        sample_type=SampleType.SAMPLE,
                    ),
                    SequenceEntry(
                        vial_location=loc2,
                        sample_name="P1-A3",
                        method=DEFAULT_METHOD,
                        inj_source=InjectionSource.HIP_ALS,
                        inj_vol=0.5,
                        num_inj=1,
                        sample_type=SampleType.SAMPLE,
                    ),
                ],
            )
            self.hplc_controller.edit_sequence(seq_table)
            self.hplc_controller.method_controller.switch(DEFAULT_METHOD)
            rand_method = MethodDetails(
                name=DEFAULT_METHOD,
                params=HPLCMethodParams(organic_modifier=5, flow=0.65),
                timetable=[
                    TimeTableEntry(start_time=0.5, organic_modifer=50, flow=0.65)
                ],
                stop_time=1,
                post_time=0.5,
            )
            self.hplc_controller.edit_method(rand_method, save=True)
            self.hplc_controller.preprun()
            self.hplc_controller.run_sequence(stall_while_running=False)
            time_left, done = self.hplc_controller.check_sequence_complete()
            while not done:
                time.sleep(time_left / 2)
                time_left, done = self.hplc_controller.check_sequence_complete()
            chrom = self.hplc_controller.get_last_run_sequence_data()
            uv = self.hplc_controller.get_last_run_sequence_data(read_uv=True)
            reports = self.hplc_controller.get_last_run_sequence_reports()
            report_vials = [reports[0].vial_location, reports[1].vial_location]
            self.assertTrue(loc1 in report_vials)
            self.assertTrue(loc2 in report_vials)
            self.assertEqual(len(chrom), 2)
            self.assertEqual(len(uv), 2)
        except Exception:
            self.fail("Failed")


if __name__ == "__main__":
    unittest.main()
