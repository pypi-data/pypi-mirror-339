import pathlib
from abc import ABCMeta, abstractmethod
from os import PathLike

import pydre.core
import polars as pl
import re
from loguru import logger
from collections.abc import Iterable


class ROIProcessor(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, filename: PathLike, nameprefix: str = ""):
        pass

    @abstractmethod
    def split(
        self, sourcedrivedata: pydre.core.DriveData
    ) -> Iterable[pydre.core.DriveData]:
        """Splits the drivedata object according to the ROI specifications.

        Parameters:
            sourcedrivedata: input drivedata object

        Returns:
            list of drivedata objects after splitting
        """
        pass


def sliceByTime(
    begin: float, end: float, column: str, drive_data: pl.DataFrame
) -> pl.DataFrame:
    """
        args:
            begin: float defnining the start point of the slice
            end: float defining the end part of the slice
            column: which column in the drive_data frame to use for the time.  This is usually SimTime or VidTime.
            drive_data: polars DataFrame containing the data to be sliced

        returns:
            polars.DataFrame slice containing requested time slice

    Given a start and end and a column name that represents a time value, output the slice that contains
    only the specified data.
    """
    try:
        dataframeslice = drive_data.filter(
            pl.col(column).is_between(begin, end, closed="left")
        )
    except KeyError:
        logger.error("Problem in applying Time ROI to using time column " + column)
        dataframeslice = drive_data
    return dataframeslice


class TimeROI(ROIProcessor):
    rois: dict
    rois_meta: set
    timecol: str

    def __init__(self, filename: PathLike, timecol: str = "DatTime"):
        # parse time filename values
        pl_rois = pl.read_csv(filename)
        rois = []
        self.rois = {}
        self.rois_meta = set()
        self.timecol = timecol
        for r in pl_rois.rows(named=True):
            if isinstance(r, dict):
                rois.append(r)
            elif isinstance(r, tuple):
                rois.append(r._asdict())
        for r in rois:
            roi_name = r["ROI"]
            self.rois[roi_name] = {}
            for k, v in r.items():
                if k == "time_start" or k == "time_end":
                    self.rois[roi_name][k] = self.parseDuration(v)
                elif k != "ROI":
                    self.rois[roi_name][k] = v
                    self.rois_meta.add(k)

    def split(
        self, sourcedrivedata: pydre.core.DriveData
    ) -> list[pydre.core.DriveData]:
        """
        return list of pydre.core.DriveData objects
        the 'roi' field of the objects will be filled with the roi tag listed
        in the roi definition file column name
        """
        output_list = []
        matching_rois = self.rois.copy()
        if len(self.rois_meta) > 0:
            for k, v in self.rois.items():
                for meta in self.rois_meta:
                    if type(v[meta]) != str:
                        if v[meta] != float(sourcedrivedata.metadata[meta]):
                            del matching_rois[k]
                            break
                    elif v[meta] != sourcedrivedata.metadata[meta]:
                        del matching_rois[k]
                        break

        for k, v in matching_rois.items():
            start = v["time_start"]
            end = v["time_end"]
            timecol = self.timecol
            new_data = sliceByTime(start, end, timecol, sourcedrivedata.data)
            if new_data.height > 0:
                new_ddata = pydre.core.DriveData(sourcedrivedata, new_data)
                new_ddata.roi = k
                output_list.append(new_ddata)
            else:
                logger.warning(
                    "ROI fails to qualify for {}, ignoring data".format(
                        sourcedrivedata.sourcefilename
                    )
                )
        return output_list

    def parseDuration(self, duration: str) -> float:
        # parse a string indicating duration into a tuple of (starttime, endtime) in seconds
        # the string will have the format as:
        # time1-time2 where time1 or time 2 are either hr:min:sec or min:sec
        # example:  1:15:10-1:20:30
        # example : 02:32-08:45

        regex = r"(?:(\d{1,2}):)?(\d{1,2}):(\d{2})"
        pair_result = re.match(regex, duration)
        if pair_result is None:
            logger.error(f"Invalid time format {duration}")
            raise ValueError
        if pair_result.group(3):
            hr = pair_result.group(1)
            min = pair_result.group(2)
            sec = pair_result.group(3)
            time = int(hr) * 60 * 60 + int(min) * 60 + int(sec)
        else:
            min = pair_result.group(1)
            sec = pair_result.group(2)
            time = 60 * 60 + int(min) * 60 + int(sec)
        return time


class SpaceROI(ROIProcessor):
    x_column_name = "XPos"
    y_column_name = "YPos"

    def __init__(self, filename: PathLike, nameprefix: str = ""):
        # parse time filename values
        # roi_info is a data frame containing the cutoff points for the region in each row.
        # It's columns must be roi, X1, X2, Y1, Y2
        pl_rois = pl.read_csv(filename, has_header=True)
        expected_columns = ["roi", "X1", "X2", "Y1", "Y2"]
        if not set(expected_columns).issubset(set(pl_rois.columns)):
            logger.error(
                f"SpaceROI file {filename} does not contain expected columns {expected_columns}"
            )
            raise ValueError
        # convert polars table into dictionary with 'roi' as the key and a dict as the value
        self.roi_info = pl_rois.rows_by_key("roi", unique=True, named=True)
        self.name_prefix = nameprefix

    def split(
        self, sourcedrivedata: pydre.core.DriveData
    ) -> Iterable[pydre.core.DriveData]:
        return_list: list[pydre.core.DriveData] = []

        for roi_name, roi_location in self.roi_info.items():
            try:
                xmin = min(roi_location.get("X1"), roi_location.get("X2"))
                xmax = max(roi_location.get("X1"), roi_location.get("X2"))
                ymin = min(roi_location.get("Y1"), roi_location.get("Y2"))
                ymax = max(roi_location.get("Y1"), roi_location.get("Y2"))
            except KeyError:
                logger.error(
                    f"ROI {roi_name} does not contain expected columns {self.roi_info.columns}"
                )
                return return_list
            except TypeError as e:
                logger.error(f"ROI {roi_name} has bad datatype: {e.args}")
                return return_list

            region_data = sourcedrivedata.data.filter(
                pl.col(self.x_column_name).cast(pl.Float32).is_between(xmin, xmax)
                & pl.col(self.y_column_name).cast(pl.Float32).is_between(ymin, ymax)
            )

            if region_data.height == 0:
                logger.warning(
                    "No data for SubjectID: {}, Source: {},  ROI: {}".format(
                        sourcedrivedata.metadata["ParticipantID"],
                        sourcedrivedata.sourcefilename,
                        roi_name,
                    )
                )
            else:
                logger.info(
                    "{} Line(s) read into ROI {} for Subject {} From file {}".format(
                        region_data.height,
                        roi_name,
                        sourcedrivedata.metadata["ParticipantID"],
                        sourcedrivedata.sourcefilename,
                    )
                )
            new_ddata = pydre.core.DriveData(sourcedrivedata, region_data)
            new_ddata.roi = roi_name
            return_list.append(new_ddata)

        return return_list


class ColumnROI(ROIProcessor):
    def __init__(self, columnname: PathLike, nameprefix=""):
        # parse time filename values
        self.roi_column: str = str(columnname)
        self.name_prefix: str = nameprefix

    def split(
        self, sourcedrivedata: pydre.core.DriveData
    ) -> Iterable[pydre.core.DriveData]:
        return_list: list[pydre.core.DriveData] = []

        for gname, gdata in sourcedrivedata.data.group_by(self.roi_column):
            gname = gname[0]
            if gname != pl.Null:
                new_ddata = pydre.core.DriveData(sourcedrivedata, gdata)
                new_ddata.roi = str(gname)
                return_list.append(new_ddata)
        return return_list
