from dataclasses import dataclass
from typing import Any

from .centerLinePoints import get_center_line_points
from .lane import calculate_borders, calculate_lanes, calculate_s_index, get_lane_class, get_lane_subtype


@dataclass(repr=False)
class Road:
    lanes: dict
    location: Any = None
    borders: Any = None
    boundaries: Any = None
    centerline_points: Any = None


def process_road(roads, road, my_opendrive, step_size, lookup_table, reference_table):
    # get centerline points, needs to be truncated later in case of multiple lane sections
    center_line_points, clp_no_offset, n_coordinates_per_segment = get_center_line_points(road, step_size)

    for i in range(0, len(road.lanes.lane_section)):
        start_point_index = calculate_s_index(center_line_points, road.lanes.lane_section[i].s)
        if i < len(road.lanes.lane_section) - 1:
            end_point_index = calculate_s_index(center_line_points, road.lanes.lane_section[i + 1].s)
        else:
            end_point_index = len(center_line_points) - 1

        my_road = Road(lanes={}, borders={}, boundaries={})

        my_road, lookup_table, reference_table = extract_road_data(
            i,
            center_line_points,
            end_point_index,
            start_point_index,
            my_road,
            road,
            lookup_table,
            len(roads),
            my_opendrive.junction_group,
            reference_table,
            clp_no_offset,
            step_size,
        )
        # insert into my_roads structure
        my_road.centerline_points = center_line_points
        roads.update({len(roads): my_road})

    return roads, lookup_table, reference_table


def extract_road_data(
    index,
    center_line_points,
    end_point_index,
    start_point_index,
    my_road,
    road,
    lookup_table,
    vvm_road_id,
    junction_group,
    reference_table,
    clp_no_offset,
    step_size,
):
    """
    Extracts all data from the input road, including geometrical data as its borders polyline as well es every other
    informations stored within.
    :param step_size:
    :param clp_no_offset:
    :param index: lane_section_index
    :param center_line_points: table of center_line_points [s,x,y,hdg,z,superelevation]
    :param end_point_index: lane_sections end point index in center_line_points table
    :param start_point_index: lane_sections start point index in center_line_points table
    :param my_road: vvm_road
    :param road: opendrive_road
    :param lookup_table: [opendrive_road_id, opendrive_lanesection_id, opendrive_lane_id, vvm_road_id, vvm_lane_id]
    :param vvm_road_id:
    :param junction_group:
    :param reference_table:
    :return:
    """
    # get borders for index lane section
    my_road = calculate_borders(
        road.lanes.lane_section[index], center_line_points, end_point_index, start_point_index, my_road, road, step_size
    )

    # get lane class (junction etc.)
    lane_class = get_lane_class(road.junction, junction_group)

    # get lane subtype (bridge, tunnel)
    lane_subtype = get_lane_subtype(road)

    # get actual lanes
    my_road, lookup_table = calculate_lanes(
        road.lanes.lane_section[index], my_road, road.id, index, lookup_table, vvm_road_id, lane_class, lane_subtype
    )

    return my_road, lookup_table, reference_table
