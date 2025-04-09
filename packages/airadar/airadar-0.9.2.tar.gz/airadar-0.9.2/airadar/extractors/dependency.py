import abc
import pathlib
import json
from enum import Enum
from typing import Optional, Any

from cyclonedx_py.parser.environment import EnvironmentParser
from cyclonedx.model.bom import Bom
from cyclonedx.output import get_instance, OutputFormat


class Extractor(abc.ABC):
    @abc.abstractmethod
    def get_report(self) -> object:
        raise NotImplementedError


class PackageDependencyType(Enum):
    ENVIRONMENT = 1
    PIP_LOCK_FILE = 2
    POETRY_LOCK_FILE = 3
    REQUIREMENTS_TXT_FILE = 4
    CONDA_LIST_FILE = 5
    CONDA_EXPLICIT_LIST_FILE = 6


class DependencyExtractor(Extractor):
    def __init__(
        self,
        package_type: PackageDependencyType,
        dependency_file_path: Optional[pathlib.Path] = None,
    ):
        if package_type != PackageDependencyType.ENVIRONMENT:
            raise NotImplementedError("Only environment extractor is available.")

        self._package_type = package_type
        self._dependency_file_path = dependency_file_path
        self.components = None

    def get_report(self) -> Any:
        if self.components:
            return self.components

        parser = EnvironmentParser()
        bom = Bom.from_parser(parser)
        json_bom = get_instance(bom, OutputFormat.JSON).output_as_string()

        return json.loads(json_bom)
