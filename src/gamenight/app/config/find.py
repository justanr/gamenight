import ast
import os
import re
from pathlib import Path
from types import ModuleType

from werkzeug.utils import ImportStringError, import_string

# probably not 100% accurate but should be good enough
_QUALNAME_RE = re.compile(r"^([_a-zA-Z]\w+\.?)+$")

CONFIG_FILE_NAME = "gamenight.cfg"


class ConfigurationError(Exception):
    pass


def config_from_path(app, path=None):
    # no path provided, let's root around in the project directory
    # looking for the default config filename
    if path is None:
        return root_around(app, CONFIG_FILE_NAME)

    if is_qualname_path(path):
        try:
            return import_string(path)
        except ImportStringError as e:
            raise ConfigurationError(f"Could not configure from {path}") from e

    path = Path(path)

    if path.absolute().exists():
        return path.absolute()

    cfg = root_around(app, path)

    if cfg is None:
        # throw here because the user explicitly provided a path instead
        # of use deciding to dig around
        raise ConfigurationError(f"Could not configure from {str(path)}")

    return cfg


def root_around(app, filename):
    return find_in_project_path(filename) or look_in_instance_path(app, filename)


def is_qualname_path(path):
    return bool(_QUALNAME_RE.match(path))


def find_in_project_path(filename):
    """
    This would most likely be the case in local development and running the
    gamenight development server.
    """
    # need to walk back to at src/.. (whatever name we've been cloned under)
    # this puts us at {name}/src/gamenight/app, we'll check our next three
    # parents for the config file
    dir = _here().parent

    for _ in range(3):
        dir = dir.parent
        cfg = dir / filename
        if cfg.exists():
            return cfg

    # alright, one more place, it *might* be in the config directory
    # that means someone modified our package structure though :|
    # this might make sense to put in the search above, but that would
    # mean also looking in gamenight.app and the cfg *shouldn't* ever
    # be there -- cue incoming bug report though
    cfg = _here() / filename

    if cfg.exists():
        return cfg


def look_in_instance_path(app, filename):
    cfg = Path(app.instance_path) / filename
    if cfg.exists():
        return cfg


def _here():
    return Path(os.path.dirname(__file__))


def config_from_env(prefix, ignore=frozenset()):
    config = {}
    for key, value in os.environ.items():
        if key in ignore:
            continue

        if key.startswith(prefix):
            try:
                value = ast.literal_eval(value)
            except Exception:
                pass
            else:
                config[key.replace(prefix, "")] = value
    return config


def getqualname(obj):
    if isinstance(obj, ModuleType):
        return obj.__package__
    return ".".join([obj.__module__, obj.__qualname__])
