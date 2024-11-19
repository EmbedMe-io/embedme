import importlib
import logging
import sys

_LOGGER = logging.getLogger(__name__)


def check_venv():
    # First check for the presence of embedme
    if importlib.util.find_spec("esphome.embedme"):
        return True

    # Are we running in a venv?
    if sys.prefix != sys.base_prefix:
        if importlib.util.find_spec("esphome"):
            _LOGGER.error(
                "EmbedMe should be run in a venv with the EmbedMe version of esphome installed"
            )
            _LOGGER.error(
                "This venv (%s)has a different version of esphome installed", sys.prefix
            )
            return False

        return True
    # TODO create and populate a venv
    _LOGGER.error("EmbedMe should be run in a venv (virtual environment)")
    return False


def run_embedme():
    from esphome.__main__ import run_esphome
    from esphome.core import EsphomeError

    try:
        return run_esphome(sys.argv)
    except EsphomeError as e:
        _LOGGER.error(e)
        return 1
    except KeyboardInterrupt:
        return 1


def main():
    if not check_venv():
        return 1
    return run_embedme()


if __name__ == "__main__":
    sys.exit(main())
