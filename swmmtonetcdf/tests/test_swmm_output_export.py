import gc
from datetime import datetime
import unittest
from swmmtonetcdf.tests.data import TRIVIAL_OUTPUT
from swmmtonetcdf import create_netcdf_from_swmm
import numpy as np
from swmm.toolkit import output, shared_enum

import netCDF4 as nc
from swmmtonetcdf import get_swmm_output_dates
import cftime


class TestSWMMtoNetCDFBySeries(unittest.TestCase):
    netcdf_output_by_series: nc.Dataset = None
    swmm_output_handle = None
    project_size = None
    num_steps = None

    @classmethod
    def setUpClass(cls) -> None:
        netcdf_output_file_by_series = TRIVIAL_OUTPUT.replace('.out', '_by_series.nc')
        create_netcdf_from_swmm(TRIVIAL_OUTPUT, netcdf_output_file_by_series, read_by_series=True)

        cls.netcdf_output_by_series = nc.Dataset(filename=netcdf_output_file_by_series, mode='r')

        cls.swmm_output_handle = output.init()
        output.open(cls.swmm_output_handle, TRIVIAL_OUTPUT)

        cls.project_size = output.get_proj_size(cls.swmm_output_handle)
        cls.num_steps = output.get_times(cls.swmm_output_handle, shared_enum.Time.NUM_PERIODS)
        cls.dates = get_swmm_output_dates(file_handle=cls.swmm_output_handle)
        cls.dates = cftime.date2num(
            [datetime.fromtimestamp(t) for t in cls.dates],
            units="hours since 0001-01-01 00:00:00.0",
            calendar="gregorian"
        )
        print()

    def test_read_output_times(self):
        times = TestSWMMtoNetCDFBySeries.netcdf_output_by_series.variables['time'][:]
        np.testing.assert_almost_equal(TestSWMMtoNetCDFBySeries.dates, times.data)

    def test_read_system_outputs(self):
        for enum_value in shared_enum.SystemAttribute:
            swmm_values = output.get_system_series(
                p_handle=TestSWMMtoNetCDFBySeries.swmm_output_handle,
                attr=enum_value,
                startPeriod=0,
                endPeriod=TestSWMMtoNetCDFBySeries.num_steps
            )

            swmm_values = np.array(swmm_values)

            netcdf_values = TestSWMMtoNetCDFBySeries.netcdf_output_by_series.variables['system_timeseries'][
                            enum_value.value,
                            :]

            np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
            gc.collect()

    def test_read_node_outputs(self):
        num_elements = TestSWMMtoNetCDFBySeries.project_size[shared_enum.ElementType.NODE.value]
        for i in range(num_elements):
            for enum_value in shared_enum.NodeAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_node_series(
                        p_handle=TestSWMMtoNetCDFBySeries.swmm_output_handle,
                        nodeIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDFBySeries.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDFBySeries.netcdf_output_by_series.variables['node_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    def test_read_link_outputs(self):
        num_elements = TestSWMMtoNetCDFBySeries.project_size[shared_enum.ElementType.LINK.value]
        for i in range(num_elements):
            for enum_value in shared_enum.LinkAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_link_series(
                        p_handle=TestSWMMtoNetCDFBySeries.swmm_output_handle,
                        linkIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDFBySeries.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDFBySeries.netcdf_output_by_series.variables['link_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    def test_read_catchment_outputs(self):
        num_elements = TestSWMMtoNetCDFBySeries.project_size[shared_enum.ElementType.SUBCATCH.value]
        for i in range(num_elements):
            for enum_value in shared_enum.SubcatchAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_subcatch_series(
                        p_handle=TestSWMMtoNetCDFBySeries.swmm_output_handle,
                        subcatchIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDFBySeries.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDFBySeries.netcdf_output_by_series.variables['catchment_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.netcdf_output_by_series.close()
        output.close(cls.swmm_output_handle)


class TestSWMMtoNetCDFByNative(unittest.TestCase):
    netcdf_output_by_native: nc.Dataset = None
    swmm_output_handle = None
    project_size = None
    num_steps = None

    @classmethod
    def setUpClass(cls) -> None:
        netcdf_output_file_by_native = TRIVIAL_OUTPUT.replace('.out', '_by_series.nc')
        create_netcdf_from_swmm(TRIVIAL_OUTPUT, netcdf_output_file_by_native, read_by_series=False)
        cls.netcdf_output_by_native = nc.Dataset(filename=netcdf_output_file_by_native, mode='r')

        cls.swmm_output_handle = output.init()
        output.open(cls.swmm_output_handle, TRIVIAL_OUTPUT)

        cls.project_size = output.get_proj_size(cls.swmm_output_handle)
        cls.num_steps = output.get_times(cls.swmm_output_handle, shared_enum.Time.NUM_PERIODS)
        cls.dates = get_swmm_output_dates(file_handle=cls.swmm_output_handle)
        cls.dates = cftime.date2num(
            [datetime.fromtimestamp(t) for t in cls.dates],
            units="hours since 0001-01-01 00:00:00.0",
            calendar="gregorian"
        )
        print()

    def test_read_output_times(self):
        times = TestSWMMtoNetCDFByNative.netcdf_output_by_native.variables['time'][:]
        np.testing.assert_almost_equal(TestSWMMtoNetCDFByNative.dates, times.data)

    def test_read_system_outputs(self):
        for enum_value in shared_enum.SystemAttribute:
            swmm_values = output.get_system_series(
                p_handle=TestSWMMtoNetCDFByNative.swmm_output_handle,
                attr=enum_value,
                startPeriod=0,
                endPeriod=TestSWMMtoNetCDFByNative.num_steps
            )

            swmm_values = np.array(swmm_values)

            netcdf_values = TestSWMMtoNetCDFByNative.netcdf_output_by_native.variables['system_timeseries'][
                            enum_value.value,
                            :]

            np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
            gc.collect()

    def test_read_node_outputs(self):
        num_elements = TestSWMMtoNetCDFByNative.project_size[shared_enum.ElementType.NODE.value]
        for i in range(num_elements):
            for enum_value in shared_enum.NodeAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_node_series(
                        p_handle=TestSWMMtoNetCDFByNative.swmm_output_handle,
                        nodeIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDFByNative.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDFByNative.netcdf_output_by_native.variables['node_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    def test_read_link_outputs(self):
        num_elements = TestSWMMtoNetCDFByNative.project_size[shared_enum.ElementType.LINK.value]
        for i in range(num_elements):
            for enum_value in shared_enum.LinkAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_link_series(
                        p_handle=TestSWMMtoNetCDFByNative.swmm_output_handle,
                        linkIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDFByNative.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDFByNative.netcdf_output_by_native.variables['link_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    def test_read_catchment_outputs(self):
        num_elements = TestSWMMtoNetCDFByNative.project_size[shared_enum.ElementType.SUBCATCH.value]
        for i in range(num_elements):
            for enum_value in shared_enum.SubcatchAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_subcatch_series(
                        p_handle=TestSWMMtoNetCDFByNative.swmm_output_handle,
                        subcatchIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDFByNative.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDFByNative.netcdf_output_by_native.variables['catchment_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.netcdf_output_by_native.close()
        output.close(cls.swmm_output_handle)
