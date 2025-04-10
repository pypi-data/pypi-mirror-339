import copy
import json
import traceback
from os import PathLike

import polars as pl
import re
import sys
import tomllib
from typing import Optional
import pydre.core
import pydre.rois
import pydre.metrics
from pydre.core import DriveData
from pydre.metrics import *
import pydre.filters
from pydre.filters import *
import pathlib
from pathlib import Path
from loguru import logger
from tqdm import tqdm
import concurrent.futures
import importlib.util


class Project:
    project_filename: Path  # used only for information
    definition: dict
    results: Optional[pl.DataFrame]
    filelist: list[Path]

    def __init__(
        self,
        projectfilename: str,
        additional_data_paths: Optional[list[str]] = None,
        outputfile: Optional[str] = None,
    ):
        self.project_filename = pathlib.Path(projectfilename)
        self.definition = {}
        self.config = {}
        self.results = None
        try:
            with open(self.project_filename, "rb") as project_file:
                if self.project_filename.suffix == ".json":
                    try:
                        self.definition = json.load(project_file)
                    except json.decoder.JSONDecodeError as e:
                        logger.exception(
                            "Error parsing JSON in {}".format(self.project_filename),
                            exception=e,
                        )
                        # exited as a general error because it is seemingly best suited for the problem encountered
                        sys.exit(1)
                elif self.project_filename.suffix == ".toml":
                    try:
                        self.definition = tomllib.load(project_file)
                    except tomllib.TOMLDecodeError as e:
                        logger.exception(
                            "Error parsing TOML in {}".format(self.project_filename),
                            exception=e,
                        )
                    # convert toml to previous project structure:
                    new_definition = {}
                    if "rois" in self.definition.keys():
                        new_definition["rois"] = Project.__restructureProjectDefinition(
                            self.definition["rois"]
                        )
                    if "metrics" in self.definition.keys():
                        new_definition["metrics"] = (
                            Project.__restructureProjectDefinition(
                                self.definition["metrics"]
                            )
                        )
                    if "filters" in self.definition.keys():
                        new_definition["filters"] = (
                            Project.__restructureProjectDefinition(
                                self.definition["filters"]
                            )
                        )
                    if "config" in self.definition.keys():
                        self.config = self.definition["config"]
                    extraKeys = set(self.definition.keys()) - {
                        "filters",
                        "rois",
                        "metrics",
                        "config",
                    }

                    if len(extraKeys) > 0:
                        logger.warning(
                            "Found unhandled keywords in project file:" + str(extraKeys)
                        )

                    self.definition = new_definition
                else:
                    logger.error("Unsupported project file type")
                    raise
        except FileNotFoundError as e:
            logger.error(f"File '{projectfilename}' not found.")
            raise e

        if additional_data_paths is not None:
            self.config["datafiles"] = (
                self.config.get("datafiles", []) + additional_data_paths
            )

        if "outputfile" in self.config:
            if outputfile is not None:
                self.config["outputfile"] = outputfile
        else:
            if outputfile is not None:
                self.config["outputfile"] = outputfile
            else:
                self.config["outputfile"] = "out.csv"

        if len(self.config.get("datafiles", [])) == 0:
            logger.error("No datafile found in project definition.")

        self._load_custom_functions()

        # resolve the file paths
        self.filelist = []
        for fn in self.config.get("datafiles", []):
            # convert relative path to absolute path
            datapath = pathlib.Path(fn).resolve()
            datafiles = datapath.parent.glob(datapath.name)
            self.filelist.extend(datafiles)

        ignore_files = []
        for fn in self.config.get("ignore", []):
            # convert relative path to absolute path
            datapath = pathlib.Path(fn).resolve()
            datafiles = datapath.parent.glob(datapath.name)
            ignore_files.extend(datafiles)

        check_lists = []
        for data_file in self.filelist:
            if data_file not in ignore_files:
                check_lists.append(data_file)
        self.filelist = check_lists

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.definition == other.definition
                and self.results == other.results
                and self.config == other.config
            )
        else:
            return False

    @staticmethod
    def __restructureProjectDefinition(def_dict: dict) -> list:
        new_def = []
        for k, v in def_dict.items():
            v["name"] = k
            new_def.append(v)
        return new_def

    def _load_custom_functions(self):
        """
        Process custom metrics and filters directories specified in the config and load metrics.
        """
        custom_metrics_dirs = self.config.get("custom_metrics_dirs", [])

        if isinstance(custom_metrics_dirs, str):
            custom_metrics_dirs = [custom_metrics_dirs]

        for metrics_dir in custom_metrics_dirs:
            metrics_path = self.resolve_file(metrics_dir)
            if not metrics_path.exists():
                logger.warning(f"Custom metrics directory not found: {metrics_path}")
                continue

            logger.info(f"Loading custom metrics from: {metrics_path}")

            # Process all Python files in the directory
            for metrics_file in metrics_path.glob("*.py"):
                try:
                    # Create a module name
                    module_name = f"custom_metrics_{metrics_file.stem}"
                    spec = importlib.util.spec_from_file_location(
                        module_name, metrics_file
                    )
                    if spec is None or spec.loader is None:
                        logger.error(f"Could not load spec for {metrics_file}")
                        continue

                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # The @registerMetric decorator will automatically register the metrics
                    logger.info(f"Successfully loaded metrics from {metrics_file}")
                except Exception as e:
                    logger.exception(
                        f"Error loading custom metrics from {metrics_file}: {e}"
                    )

        custom_filters_dirs = self.config.get("custom_filters_dirs", [])

        if isinstance(custom_filters_dirs, str):
            custom_filters_dirs = [custom_filters_dirs]
        for filters_dir in custom_filters_dirs:
            filters_path = self.resolve_file(filters_dir)
            if not filters_path.exists():
                logger.warning(f"Custom filters directory not found: {filters_path}")
                continue
            logger.info(f"Loading custom filters from: {filters_path}")
            for filters_file in filters_path.glob("*.py"):
                try:
                    module_name = f"custom_filters_{filters_file.stem}"
                    spec = importlib.util.spec_from_file_location(
                        module_name, filters_file
                    )
                    if spec is None or spec.loader is None:
                        logger.error(f"Could not load spec for {filters_file}")
                        continue
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    logger.info(f"Successfully loaded filters from {filters_file}")
                except Exception as e:
                    logger.exception(
                        f"Error loading custom filters from {filters_file}: {e}"
                    )

    def resolve_file(self, pathname: PathLike) -> pathlib.Path:
        """Resolve the given file to an absolute path based on the project file location.
        Args:
            pathname: A string or Path object.
        Returns:
            A pathlib.Path object representing the resolved metrics directory.
        """
        computed_path = pathlib.Path(pathname)
        if computed_path.is_absolute():
            computed_path = computed_path.resolve()
        else:
            computed_path = pathlib.Path(
                self.project_filename.parent / computed_path
            ).resolve()
        return computed_path

    @staticmethod
    def processROI(
        roi: dict, datafile: pydre.core.DriveData
    ) -> list[pydre.core.DriveData]:
        """
        Handles running region of interest definitions for a dataset

        Args:
                roi: A dict containing the type of a roi and the filename of the data used to process it
                datafile: drive data object to process with the roi

        Returns:
                A list of drivedata objects containing the data for each region of interest
        """
        roi_obj: pydre.rois.ROIProcessor
        roi_type = roi["type"]
        if roi_type == "time":
            logger.info("Processing time ROI " + roi["filename"])
            if "timecol" in roi:
                roi_obj = pydre.rois.TimeROI(roi["filename"], roi["timecol"])
            else:
                roi_obj = pydre.rois.TimeROI(roi["filename"])
        elif roi_type == "rect":
            logger.info("Processing space ROI " + roi["filename"])
            roi_obj = pydre.rois.SpaceROI(roi["filename"])
        elif roi_type == "column":
            logger.info("Processing column ROI " + roi["columnname"])
            roi_obj = pydre.rois.ColumnROI(roi["columnname"])
        else:
            logger.warning("Unknown ROI type {}".format(roi_type))
            return [datafile]
        return roi_obj.split(datafile)

    @staticmethod
    def processFilter(
        datafilter: dict, datafile: pydre.core.DriveData
    ) -> pydre.core.DriveData:
        """
        Handles running any filter definition

        Args:
            datafilter: A dict containing the function of a filter and the parameters to process it
            datafile: drive data object to process with the filter

        Returns:
            The augmented DriveData object
        """
        ldatafilter = copy.deepcopy(datafilter)
        try:
            func_name = ldatafilter.pop("function")
            filter_func = pydre.filters.filtersList[func_name]
            datafilter_name = ldatafilter.pop("name")
        except KeyError as e:
            logger.error(
                'Filter definitions require a "function". Malformed filters definition: missing '
                + str(e)
            )
            raise e

        return filter_func(datafile, **ldatafilter)

    def processMetric(self, metric: dict, dataset: pydre.core.DriveData) -> dict:
        """
        Handles running any metric definition

        Args:
            metric: A dict containing the function of a metric and the parameters to process it
            dataset: drive data object to process with the metric

        Returns:
            A dictionary containing the results of the metric
        """

        metric = copy.deepcopy(metric)
        try:
            func_name = metric.pop("function")
            metric_func = pydre.metrics.metricsList[func_name]
            report_name = metric.pop("name")
            col_names = pydre.metrics.metricsColNames[func_name]
        except KeyError as e:
            logger.warning(
                'Metric definitions require both "name" and "function". Malformed metrics definition'
            )
            raise e

        metric_dict = dict()
        if len(col_names) > 1:
            x = metric_func(dataset, **metric)
            metric_dict = dict(zip(col_names, x))
        else:
            # report = pl.DataFrame(
            #    [metric_func(dataset, **metric) ], schema=[report_name, ])
            metric_dict[report_name] = metric_func(dataset, **metric)
        return metric_dict

    @staticmethod
    def __clean(src_str: str) -> str:
        """
        Remove any parenthesis, quote mark and un-necessary directory names from a string
        """
        return (
            src_str.replace("[", "").replace("]", "").replace("'", "").split("\\")[-1]
        )

    def processDatafiles(self, numThreads: int = 12) -> Optional[pl.DataFrame]:
        """Load all metrics, then iterate over each file and process the filters, rois, and metrics for each.

        Args:
            numThreads: number of threads to run simultaneously in the thread pool

        Returns:
            metrics data for all metrics, or None on error

        """
        if "metrics" not in self.definition:
            logger.critical("No metrics in project file. No results will be generated")
            return None
        results_list = []
        with tqdm(total=len(self.filelist)) as pbar:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=numThreads
            ) as executor:
                futures = {
                    executor.submit(self.processSingleFile, singleFile): singleFile
                    for singleFile in self.filelist
                }
                results = {}
                for future in concurrent.futures.as_completed(futures):
                    arg = futures[future]
                    try:
                        results[arg] = future.result()
                    except Exception as exc:
                        logger.error("problem with running {}".format(arg))
                        logger.critical("Unhandled Exception {}".format(exc))
                        logger.error(traceback.format_exc())

                    results_list.extend(future.result())
                    pbar.update(1)
        if len(results_list) == 0:
            logger.error("No results found; no metrics data generated")
        result_dataframe = pl.from_dicts(results_list)

        # sorting_columns = ["Subject", "ScenarioName", "ROI"]
        # try:
        #    result_dataframe = result_dataframe.sort(sorting_columns)
        # except pl.exceptions.PanicException as e:
        #    logger.warning("Can't sort results, must be missing a column.")

        self.results = result_dataframe
        return result_dataframe

    def processSingleFile(self, datafilename: Path):
        logger.info("Loading file {}".format(datafilename))
        if "datafile_type" in self.config:
            if self.config["datafile_type"] == "rti":
                datafile = DriveData.init_rti(datafilename)
            elif self.config["datafile_type"] == "oldrti":
                datafile = DriveData.init_old_rti(datafilename)
            elif self.config["datafile_type"] == "scanner":
                datafile = DriveData.init_scanner(datafilename)
            else:
                logger.warning(
                    f"Unknown datafile type {self.config['datafile_type']}, processing as RTI .dat file."
                )
                datafile = DriveData.init_rti(datafilename)
        else:
            datafile = DriveData.init_rti(datafilename)

        datafile.loadData()
        roi_datalist = []
        results_list = []

        if "filters" in self.definition:
            for datafilter in self.definition["filters"]:
                try:
                    datafile = self.processFilter(datafilter, datafile)
                except Exception as e:
                    logger.exception(
                        "Unhandled exception in {} while processing {}.".format(
                            datafilter, datafilename
                        )
                    )
                    raise e
        if "rois" in self.definition:
            for roi in self.definition["rois"]:
                try:
                    roi_datalist.extend(self.processROI(roi, datafile))
                except Exception as e:
                    logger.exception(
                        "Unhandled exception in {} while processing {}.".format(
                            roi, datafilename
                        )
                    )
                    raise e

        else:
            # no ROIs to process, but that's OK
            logger.warning("No ROIs defined, processing raw data.")
            roi_datalist.append(datafile)

        if len(roi_datalist) == 0:
            logger.warning(
                "Qualifying ROIs fail to generate results for {}, no output generated.".format(
                    datafilename
                )
            )
            return []

        for data in roi_datalist:
            result_dict = copy.deepcopy(datafile.metadata)
            result_dict["ROI"] = data.roi

            for metric in self.definition["metrics"]:
                try:
                    processed_metric = self.processMetric(metric, data)
                    result_dict.update(processed_metric)
                except Exception as e:
                    logger.critical(
                        "Unhandled exception {} in {} while processing {}.".format(
                            e.args, metric, datafilename
                        )
                    )
                    raise e
            results_list.append(result_dict)
        return results_list

    def saveResults(self):
        """
        Args:
            outfilename: filename to output csv data to.

            The filename specified will be overwritten automatically.
        """
        try:
            self.results.write_csv(self.config["outputfile"])
        except AttributeError:
            logger.error("Results not computed yet")
