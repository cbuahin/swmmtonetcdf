# python imports
from typing import Dict, Union
import datetime

# external imports
import julian
import numpy as np
from swmm.toolkit import output, shared_enum, output_metadata
import netCDF4 as nc
import cftime
from collections import OrderedDict


# local imports
def get_swmm_output_dates(file_handle):
    """
    Get timestamps for output file
    Args:
        file_handle: SWMM output file handle
    Returns:
        Array of timestamps for output file
    """
    num_steps = output.get_times(file_handle, shared_enum.Time.NUM_PERIODS)
    report_step = output.get_times(file_handle, shared_enum.Time.REPORT_STEP)
    report_start_date_time = output.get_start_date(file_handle)

    start_date_time = julian.from_jd(report_start_date_time + 2415018.5) + datetime.timedelta(seconds=report_step)
    end_date_time = start_date_time + datetime.timedelta(seconds=num_steps * report_step)

    date_times = np.arange(
        start=start_date_time.timestamp(),
        stop=end_date_time.timestamp(),
        step=report_step
    )

    return date_times


def get_swmm_output_element_names(file_handle, element_type: shared_enum.ElementType) -> Dict[str, int]:
    """
    Get element names

    Args:
        file_handle: SWMM output file handle
        element_type:

    Returns:

    """
    names = OrderedDict()
    project_size = output.get_proj_size(file_handle)

    count = project_size[element_type.value]
    for i in range(count):
        name = output.get_elem_name(file_handle, element_type, i)
        names[name] = i

    return names


def get_pollutant_enum_name(file_handle, pollutant_name: str) -> str:
    """
    Get name of pollutant
    Args:
        file_handle: SWMM output file handle
        pollutant_name:

    Returns:

    """
    pollutant_names = get_swmm_output_element_names(file_handle, shared_enum.ElementType.POLLUT)
    return f'POLLUT_CONC_{pollutant_names[pollutant_name]}'


def get_pollutant_enum(
        file_handle,
        element_attribute: Union[shared_enum.SubcatchAttribute,
                                 shared_enum.NodeAttribute,
                                 shared_enum.LinkAttribute,
                                 shared_enum.SystemAttribute],
        pollutant_name: str) -> Union[shared_enum.SubcatchAttribute, shared_enum.NodeAttribute,
                                      shared_enum.LinkAttribute, shared_enum.SystemAttribute]:
    """

    Get pollutant enumeration

    Args:
        file_handle:  SWMM output file handle
        element_attribute: Element type
        pollutant_name (str) : Pollutant name

    Returns:

    """
    pollutant_enum_name = get_pollutant_enum_name(file_handle, pollutant_name)
    return element_attribute[pollutant_enum_name]


def create_netcdf_from_swmm(swmm_output_file: str, netcdf_output_file: str, read_by_series=True):
    """
    Creates netcdf output from SWMM output

    Args:
        read_by_series (bool): Read whole timeseries at time

        swmm_output_file (str): SWMM output filepath

        netcdf_output_file (str): NetCDF

    Returns:

    """
    file_handle = output.init()
    output.open(p_handle=file_handle, path=swmm_output_file)
    output_metadata.OutputMetadata(file_handle)

    netcdf_output = nc.Dataset(netcdf_output_file, mode='w', format="NETCDF4")

    # output size
    project_size = output.get_proj_size(file_handle)
    num_catchments = project_size[shared_enum.ElementType.SUBCATCH.value]
    num_nodes = project_size[shared_enum.ElementType.NODE.value]
    num_links = project_size[shared_enum.ElementType.LINK.value]
    num_steps = output.get_times(file_handle, shared_enum.Time.NUM_PERIODS)
    swmm_output_timestamps = get_swmm_output_dates(file_handle=file_handle)

    # Timestamps
    netcdf_output.createDimension(dimname='time', size=None)
    nc_time_variable = netcdf_output.createVariable(
        varname="time",
        datatype=np.float,
        dimensions=("time",),

    )
    nc_time_variable.units = "hours since 0001-01-01 00:00:00.0"
    nc_time_variable.calendar = "gregorian"

    nc_time_variable[:] = cftime.date2num(
        [datetime.datetime.fromtimestamp(t) for t in swmm_output_timestamps],
        units=nc_time_variable.units,
        calendar=nc_time_variable.calendar
    )

    # Element names
    pollutants_names = get_swmm_output_element_names(file_handle=file_handle,
                                                     element_type=shared_enum.ElementType.POLLUT)

    links = get_swmm_output_element_names(file_handle=file_handle, element_type=shared_enum.ElementType.LINK)
    nodes = get_swmm_output_element_names(file_handle=file_handle, element_type=shared_enum.ElementType.NODE)
    catchments = get_swmm_output_element_names(file_handle=file_handle, element_type=shared_enum.ElementType.SUBCATCH)

    node_attributes = [r.name for r in shared_enum.NodeAttribute if 'POLLUT_CONC_' not in r.name]
    node_attributes.extend(list(pollutants_names.keys()))
    num_node_attributes = len(node_attributes)

    link_attributes = [r.name for r in shared_enum.LinkAttribute if 'POLLUT_CONC_' not in r.name]
    link_attributes.extend(list(pollutants_names.keys()))
    num_link_attributes = len(link_attributes)

    catchment_attributes = [r.name for r in shared_enum.SubcatchAttribute if 'POLLUT_CONC_' not in r.name]
    catchment_attributes.extend(list(pollutants_names.keys()))
    num_catchment_attributes = len(catchment_attributes)

    system_attributes = [r.name for r in shared_enum.SystemAttribute]
    num_system_attributes = len(system_attributes)

    netcdf_output.createDimension(dimname='nodes', size=len(nodes))
    netcdf_output.createDimension(dimname='links', size=len(links))
    netcdf_output.createDimension(dimname='catchments', size=len(catchments))

    nc_node_element_names_variable = netcdf_output.createVariable(
        varname='nodes',
        datatype=str,
        dimensions=('nodes',)
    )

    nc_link_element_names_variable = netcdf_output.createVariable(
        varname='links',
        datatype=str,
        dimensions=('links',)
    )

    nc_catchment_element_names_variable = netcdf_output.createVariable(
        varname='catchments',
        datatype=str,
        dimensions=('catchments',)
    )

    netcdf_output.createDimension(dimname='node_attributes', size=len(node_attributes))
    netcdf_output.createDimension(dimname='link_attributes', size=len(link_attributes))
    netcdf_output.createDimension(dimname='catchment_attributes', size=len(catchment_attributes))
    netcdf_output.createDimension(dimname='system_attributes', size=len(system_attributes))

    nc_node_attributes_names_variable = netcdf_output.createVariable(
        varname='node_attribute_names',
        datatype=str,
        dimensions=('node_attributes',),

    )

    nc_link_attributes_names_variable = netcdf_output.createVariable(
        varname='link_attribute_names',
        datatype=str,
        dimensions=('link_attributes',)
    )

    nc_catchment_attributes_names_variable = netcdf_output.createVariable(
        varname='catchment_attribute_names',
        datatype=str,
        dimensions=('catchment_attributes',)
    )

    nc_system_attributes_names_variable = netcdf_output.createVariable(
        varname='system_attribute_names',
        datatype=str,
        dimensions=('system_attributes',)
    )

    nc_node_timeseries = netcdf_output.createVariable(
        varname='node_timeseries',
        datatype=np.float,
        dimensions=('nodes', 'node_attributes', 'time',)
    )

    nc_link_timeseries = netcdf_output.createVariable(
        varname='link_timeseries',
        datatype=np.float,
        dimensions=('links', 'link_attributes', 'time',)
    )

    nc_catchment_timeseries = netcdf_output.createVariable(
        varname='catchment_timeseries',
        datatype=np.float,
        dimensions=('catchments', 'catchment_attributes', 'time',)
    )

    nc_system_timeseries = netcdf_output.createVariable(
        varname='system_timeseries',
        datatype=np.float,
        dimensions=('system_attributes', 'time',)
    )

    # node attributes
    nc_node_element_names_variable[:] = np.array(list(nodes.keys()), dtype=object)
    nc_node_attributes_names_variable[:] = np.array(node_attributes, dtype=object)

    # link attributes
    nc_link_element_names_variable[:] = np.array(list(links.keys()), dtype=object)
    nc_link_attributes_names_variable[:] = np.array(link_attributes, dtype=object)

    # catchment attributes
    nc_catchment_element_names_variable[:] = np.array(list(catchments.keys()), dtype=object)
    nc_catchment_attributes_names_variable[:] = np.array(catchment_attributes, dtype=object)

    # system attributes
    nc_system_attributes_names_variable[:] = np.array(system_attributes, dtype=object)

    if read_by_series:
        # catchment attributes
        for i in range(len(catchment_attributes)):
            catchment_attribute = catchment_attributes[i]
            catchment_attribute_enum = shared_enum.SubcatchAttribute[catchment_attribute]

            j: int = 0
            for catchment_id, catchment_index in catchments.items():
                catchment_series = output.get_subcatch_series(
                    p_handle=file_handle,
                    subcatchIndex=catchment_index,
                    attr=catchment_attribute_enum,
                    startPeriod=0,
                    endPeriod=num_steps
                )

                nc_catchment_timeseries[j, i, :] = np.array(catchment_series, dtype=np.float)
                netcdf_output.sync()
                j += 1

        # node attributes
        for i in range(len(node_attributes)):
            node_attribute = node_attributes[i]
            node_attribute_enum = shared_enum.NodeAttribute[node_attribute]

            j: int = 0
            for node_id, node_index in nodes.items():
                node_series = output.get_node_series(
                    p_handle=file_handle,
                    nodeIndex=node_index,
                    attr=node_attribute_enum,
                    startPeriod=0,
                    endPeriod=num_steps
                )

                nc_node_timeseries[j, i, :] = np.array(node_series, dtype=np.float)
                netcdf_output.sync()
                j += 1

        # link attributes
        for i in range(len(link_attributes)):
            link_attribute = link_attributes[i]
            link_attribute_enum = shared_enum.LinkAttribute[link_attribute]

            j: int = 0
            for link_id, link_index in links.items():
                link_series = output.get_link_series(
                    p_handle=file_handle,
                    linkIndex=link_index,
                    attr=link_attribute_enum,
                    startPeriod=0,
                    endPeriod=num_steps
                )

                nc_link_timeseries[j, i, :] = np.array(link_series, dtype=np.float)
                netcdf_output.sync()
                j += 1

        # system attributes
        for i in range(len(system_attributes)):
            system_attribute = system_attributes[i]
            system_attribute_enum = shared_enum.SystemAttribute[system_attribute]

            system_series = output.get_system_series(
                p_handle=file_handle,
                attr=system_attribute_enum,
                startPeriod=0,
                endPeriod=num_steps
            )

            nc_system_timeseries[i, :] = np.array(system_series)
            netcdf_output.sync()
    else:
        for t in range(num_steps):
            # catchment attributes
            for j in range(num_catchments):
                catchment_results = output.get_subcatch_result(p_handle=file_handle, timeIndex=t, subcatchIndex=j)
                nc_catchment_timeseries[j, :, t] = np.array(catchment_results[0:num_catchment_attributes],
                                                            dtype=np.float)

            # node attributes
            for j in range(num_nodes):
                node_results = output.get_node_result(p_handle=file_handle, timeIndex=t, nodeIndex=j)
                nc_node_timeseries[j, :, t] = np.array(node_results[0:num_node_attributes], dtype=np.float)

            # link attributes
            for j in range(num_links):
                link_results = output.get_link_result(p_handle=file_handle, timeIndex=t, linkIndex=j)
                nc_link_timeseries[j, :, t] = np.array(link_results[0:num_link_attributes], dtype=np.float)

            # system attributes
            system_results = output.get_system_result(p_handle=file_handle, timeIndex=t, dummyIndex=0)
            nc_system_timeseries[:, t] = np.array(system_results[0:num_system_attributes], dtype=np.float)

            if t % 5000 == 0:
                netcdf_output.sync()

            progress = int(t * 100 / num_steps)
            print(rf'Progress: {progress}%/{100}', end='\r')

    netcdf_output.close()
    output.close(file_handle)
