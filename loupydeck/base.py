"""
loupydeck base module.

This is the principal module of the loupydeck project, containing main classes and objects.

"""

import inspect
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

# TODO: Pass from CLI
logger.setLevel(logging.DEBUG)

# example constant variable
NAME = "loupydeck"


class AbstractComponent(ABC):
    """
    Defines a common interface for components.

    e.g. Devices, Applications, Profiles etc
    """
    
    _has_info = True

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent

        # Passing null to self contained property setters
        self.folder = None
        self.path = None
        self.info = None
        self.children = None

        print(f"{self._cls_name()}: {self.name=}")
        print(f"{self._cls_name()}: {self.folder=}")
        print(f"{self._cls_name()}: {self.path=}")
        print(f"{self._cls_name()}: {self.info=}")
        print(f"{self._cls_name()}: {self.children=}")

    @classmethod
    def _cls_name(cls):
        return str(cls.__name__)

    @classmethod
    def _info_file(cls):
        return f"{cls._cls_name()}Info.json"

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value=None):
        if not value:
            value = Loupedeck()

        self._parent = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        property_name = f"{self._cls_name()}.{inspect.stack()[0][3]}"
        message = None
        min_length = 5
        if not value:
            message = f"{property_name} cannot be empty"
        if len(value) < min_length:
            message = f"{property_name} cannot be shorter than {min_length}"

        if message:
            raise ValueError(message)

        self._name = value

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        if value:
            message = "Folder attribute should be set by the class"
            raise ValueError(message)

        self._folder = self.name

    @property
    def path(self):
        """Filepath for the component."""
        return self._path

    @path.setter
    def path(self, value):
        if value:
            value = Path(str(value))
        else:
            value = Path(self.parent.path, self.folder)
            # value = Path(self.parent.path)

        self._path = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, folder=None):
        path = self.path
        if folder:
            path = Path(self.path, folder)
        excludes = [".DS_Store"]
        dirs = [p.name for p in path.glob("*") if p.is_dir()]
        dirs = [d for d in dirs if d not in excludes and d[0] != "."]
        self._children = dirs

    @property
    def info(self):
        """Dictionary representation of the component config information."""
        if self._has_info:
            return self._info

    @info.setter
    def info(self, _):
        if self._has_info:
            info_path = Path(self.path, self._info_file())
            with open(info_path) as json_data:
                data = json.load(json_data)

            self._info = data


class Loupedeck:
    def __init__(self, install_location=None) -> None:
        # TODO: Defaults from config file

        user_path = Loupedeck.get_user_path()
        paths = dict(
            # TODO: Windows & Unix
            mac=".local/share/Loupedeck",
        )

        os = self._get_os()
        self.path = Path(user_path, paths[os], "Applications")
        logger.debug(f"{self.path=}")
        print(f"{self.path=}")

    @classmethod
    def get_user_path(cls):
        """Get path to user folder."""
        return str(Path.home())

    @classmethod
    def _get_os(cls):
        from sys import platform

        if platform == "linux" or platform == "linux2":
            raise NotImplementedError("OS not yet supported")
            os = "linux"
        elif platform == "darwin":
            os = "mac"
        elif platform == "win32":
            raise NotImplementedError("OS not yet supported")
            # os = "windows"
        else:
            # TODO: Warn and use a default
            message = f"Couldn't identify {platform=}"
            raise RuntimeError(message)
        return os


# class Profile:
#     def __init__(self, name, app=None):
#         if not name:
#             message = "You must provide a Profile name"
#             raise ValueError(message)

#         if not app:
#             app = Loupedeck()

#         self.app = app

#         self.path = Path(app.device_path, name)
#         print(f"{self.path=}")

#         files = self.path.glob("*")
#         print(list(files))
