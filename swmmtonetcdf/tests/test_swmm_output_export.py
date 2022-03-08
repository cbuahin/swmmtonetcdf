import gc
import unittest
from swmmtonetcdf.tests.data import TRIVIAL_OUTPUT
from swmmtonetcdf import create_netcdf_from_swmm
import numpy as np
from swmm.toolkit import output, shared_enum

import netCDF4 as nc


class TestSWMMtoNetCDF(unittest.TestCase):
    netcdf_output: nc.Dataset = None
    swmm_output_handle = None
    project_size = None
    num_steps = None

    @classmethod
    def setUpClass(cls) -> None:
        netcdf_output_file = TRIVIAL_OUTPUT.replace('.out', '.nc')
        create_netcdf_from_swmm(TRIVIAL_OUTPUT, netcdf_output_file)
        cls.netcdf_output = nc.Dataset(filename=netcdf_output_file, mode='r')
        cls.swmm_output_handle = output.init()
        output.open(cls.swmm_output_handle, TRIVIAL_OUTPUT)

        cls.project_size = output.get_proj_size(cls.swmm_output_handle)
        cls.num_steps = output.get_times(cls.swmm_output_handle, shared_enum.Time.NUM_PERIODS)

    def test_read_system_outputs(self):
        for enum_value in shared_enum.SystemAttribute:
            swmm_values = output.get_system_series(
                p_handle=TestSWMMtoNetCDF.swmm_output_handle,
                attr=enum_value,
                startPeriod=0,
                endPeriod=TestSWMMtoNetCDF.num_steps
            )

            swmm_values = np.array(swmm_values)

            netcdf_values = TestSWMMtoNetCDF.netcdf_output.variables['system_timeseries'][
                            enum_value.value,
                            :]

            np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
            gc.collect()

    def test_read_node_outputs(self):
        num_elements = TestSWMMtoNetCDF.project_size[shared_enum.ElementType.NODE.value]
        for i in range(num_elements):
            for enum_value in shared_enum.NodeAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_node_series(
                        p_handle=TestSWMMtoNetCDF.swmm_output_handle,
                        nodeIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDF.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDF.netcdf_output.variables['node_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    def test_read_link_outputs(self):
        num_elements = TestSWMMtoNetCDF.project_size[shared_enum.ElementType.LINK.value]
        for i in range(num_elements):
            for enum_value in shared_enum.LinkAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_link_series(
                        p_handle=TestSWMMtoNetCDF.swmm_output_handle,
                        linkIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDF.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDF.netcdf_output.variables['link_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    def test_read_catchment_outputs(self):
        num_elements = TestSWMMtoNetCDF.project_size[shared_enum.ElementType.SUBCATCH.value]
        for i in range(num_elements):
            for enum_value in shared_enum.SubcatchAttribute:
                if 'POLLUT_CONC' not in enum_value.name:
                    swmm_values = output.get_subcatch_series(
                        p_handle=TestSWMMtoNetCDF.swmm_output_handle,
                        subcatchIndex=i,
                        attr=enum_value,
                        startPeriod=0,
                        endPeriod=TestSWMMtoNetCDF.num_steps
                    )

                    swmm_values = np.array(swmm_values)

                    netcdf_values = TestSWMMtoNetCDF.netcdf_output.variables['catchment_timeseries'][
                                    i,
                                    enum_value.value,
                                    :]

                    np.testing.assert_almost_equal(swmm_values, netcdf_values.data)
                    gc.collect()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.netcdf_output.close()
        output.close(cls.swmm_output_handle)
