import os
import time
import unittest


from pychemstation.utils.sequence_types import (
    SequenceTable,
    SequenceEntry,
    InjectionSource,
    SampleType,
)
from pychemstation.utils.tray_types import (
    FiftyFourVialPlate,
    VialBar,
)
from tests.constants import (
    clean_up,
    set_up_utils,
    DEFAULT_METHOD_242,
    DEFAULT_METHOD_254,
    DEFAULT_SEQUENCE,
    DEFAULT_METHOD,
    VIAL_PLATES,
)


class TestSequence(unittest.TestCase):
    """
    These tests should always work with an online controller.
    """

    def setUp(self):
        num = 242
        self.hplc_controller = set_up_utils(num, offline=False, runs=False)
        self.other_default = DEFAULT_METHOD_242 if num == 242 else DEFAULT_METHOD_254
        self.hplc_controller.switch_sequence(DEFAULT_SEQUENCE)

    def tearDown(self):
        clean_up(self.hplc_controller)

    def test_run_sequence_no_stall(self):
        self.hplc_controller.preprun()
        self.hplc_controller.run_sequence(stall_while_running=False)
        time_left, done = self.hplc_controller.check_sequence_complete()
        sequence_dir = self.hplc_controller.sequence_controller.data_files[-1].dir
        child_dir = self.hplc_controller.sequence_controller.data_files[-1].child_dirs[0]
        self.assertIsNotNone(sequence_dir)
        self.assertIsNotNone(child_dir)
        self.assertTrue(os.path.isdir(sequence_dir))
        self.assertTrue(os.path.isdir(child_dir))
        while not done:
            time.sleep(time_left / 2)
            time_left, done = self.hplc_controller.check_sequence_complete()
        _ = self.hplc_controller.get_last_run_sequence_data()
        uv = self.hplc_controller.get_last_run_sequence_data(read_uv=True)
        reports = self.hplc_controller.get_last_run_sequence_reports()
        for i, report in enumerate(reports):
            self.assertIsNotNone(report.vial_location)
            self.assertIsNotNone(report.solvents)
            self.assertTrue(210 in list(uv[i].keys()))

    def test_run_sequence_stall(self):
        self.hplc_controller.preprun()
        self.hplc_controller.run_sequence(stall_while_running=True)
        time_left, done = self.hplc_controller.check_sequence_complete()
        self.assertTrue(done)
        self.assertTrue(time_left )
        sequence_dir = self.hplc_controller.sequence_controller.data_files[-1].dir
        child_dir = self.hplc_controller.sequence_controller.data_files[-1].child_dirs[0]
        self.assertIsNotNone(sequence_dir)
        self.assertIsNotNone(child_dir)
        self.assertTrue(os.path.isdir(sequence_dir))
        self.assertTrue(os.path.isdir(child_dir))
        while not done:
            time.sleep(time_left / 2)
            time_left, done = self.hplc_controller.check_sequence_complete()
        _ = self.hplc_controller.get_last_run_sequence_data()
        uv = self.hplc_controller.get_last_run_sequence_data(read_uv=True)
        reports = self.hplc_controller.get_last_run_sequence_reports()
        for i, report in enumerate(reports):
            self.assertIsNotNone(report.vial_location)
            self.assertIsNotNone(report.solvents)
            self.assertTrue(210 in list(uv[i].keys()))

    def test_tray_nums(self):
        seq_table = SequenceTable(
            name=DEFAULT_SEQUENCE,
            rows=[
                SequenceEntry(
                    vial_location=v,
                    method=DEFAULT_METHOD,
                    num_inj=3,
                    inj_vol=4,
                    sample_name=str(v.value()),
                    data_file=str(v.value()),
                    sample_type=SampleType.SAMPLE,
                    inj_source=InjectionSource.HIP_ALS,
                )
                for v in VIAL_PLATES
            ],
        )
        self.hplc_controller.edit_sequence(seq_table)
        loaded_table = self.hplc_controller.load_sequence()
        for i in range(len(VIAL_PLATES)):
            self.assertTrue(
                VIAL_PLATES[i].value()
                == seq_table.rows[i].vial_location.value()
                == loaded_table.rows[i].vial_location.value()
            )

    def test_load(self):
        try:
            seq = self.hplc_controller.load_sequence()
            self.assertTrue(len(seq.rows) > 0)
        except Exception as e:
            self.fail(f"Should have not expected: {e}")

    def test_edit_entire_seq_table(self):
        self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        meth_path = os.path.join(
            self.hplc_controller.method_controller.src, DEFAULT_METHOD
        )
        try:
            seq_table = SequenceTable(
                name=DEFAULT_SEQUENCE,
                rows=[
                    SequenceEntry(
                        vial_location=VialBar.SEVEN,
                        method=meth_path,
                        num_inj=3,
                        inj_vol=4.0,
                        sample_name="asd",
                        data_file="asd",
                        sample_type=SampleType.SAMPLE,
                        inj_source=InjectionSource.HIP_ALS,
                    ),
                    SequenceEntry(
                        vial_location=FiftyFourVialPlate.from_str("P2-F2"),
                        method=meth_path,
                        num_inj=3,
                        inj_vol=4.0,
                        sample_name="qwe",
                        data_file="qwe",
                        sample_type=SampleType.SAMPLE,
                        inj_source=InjectionSource.HIP_ALS,
                    ),
                    SequenceEntry(
                        vial_location=VialBar.ONE,
                        method=meth_path,
                        num_inj=3,
                        inj_vol=4.0,
                        sample_name="Sampel2232",
                        data_file="Sampel2232",
                        sample_type=SampleType.SAMPLE,
                        inj_source=InjectionSource.HIP_ALS,
                    ),
                ],
            )
            self.hplc_controller.edit_sequence(seq_table)
            self.assertEqual(seq_table, self.hplc_controller.load_sequence())
        except Exception:
            self.fail("Should have not occured")

    def test_switch_seq(self):
        try:
            self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        except Exception as e:
            self.fail(f"Should have not expected: {e}")

    def test_read_seq(self):
        try:
            self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
            table = self.hplc_controller.load_sequence()
            self.assertTrue(table)
        except Exception as e:
            self.fail(f"Should have not expected: {e}")

    def test_edit_specific_rows(self):
        self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        try:
            meth_path = os.path.join(
                self.hplc_controller.method_controller.src, DEFAULT_METHOD
            )
            seq_table = SequenceTable(
                name=DEFAULT_SEQUENCE,
                rows=[
                    SequenceEntry(
                        vial_location=VialBar.TEN,
                        method=meth_path,
                        num_inj=3,
                        inj_vol=4.0,
                        sample_name="Sampel2",
                        data_file="Sampel2csdf",
                        sample_type=SampleType.SAMPLE,
                        inj_source=InjectionSource.HIP_ALS,
                    ),
                    SequenceEntry(
                        vial_location=FiftyFourVialPlate.from_str("P2-F2"),
                        method=meth_path,
                        num_inj=3,
                        inj_vol=4.0,
                        sample_name="Sampel2",
                        data_file="Sampel2sdfsd",
                        sample_type=SampleType.SAMPLE,
                        inj_source=InjectionSource.HIP_ALS,
                    ),
                ],
            )
            self.hplc_controller.edit_sequence(seq_table)
            seq_table.rows[0].vial_location = FiftyFourVialPlate.from_str("P1-F3")
            seq_table.rows[1].vial_location = VialBar.THREE
            seq_table.rows[0].sample_type = SampleType.BLANK
            seq_table.rows[0].inj_source = InjectionSource.MANUAL
            self.hplc_controller.edit_sequence(seq_table)
            loaded_seq = self.hplc_controller.load_sequence()
            self.assertEqual(seq_table, loaded_seq)
            try:
                self.hplc_controller.sequence_controller.edit_sample_name("fail", 10)
                self.fail("need to throw")
            except ValueError:
                pass
        except Exception:
            self.fail("Should have not occured")


if __name__ == "__main__":
    unittest.main()
