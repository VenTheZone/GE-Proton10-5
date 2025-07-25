"""Starts the protonfix module and runs fixes after pre-flight-checks"""

import os
import sys
import traceback
from typing import Callable

from . import fix
from .logger import log

sys.path.insert(
    0,
    f'{os.path.dirname(os.path.realpath(__file__))}/_vendor',  # noqa: PTH120
)

bin_dir: str = f'{os.path.dirname(os.path.realpath(__file__))}/files/bin'
i386_lib_dir: str = (
    f'{os.path.dirname(os.path.realpath(__file__))}/files/lib/i386-linux-gnu'
)
x86_64_lib_dir: str = (
    f'{os.path.dirname(os.path.realpath(__file__))}/files/lib/x86_64-linux-gnu'
)


def check_conditions() -> bool:
    """Determine, if the actual game was executed and protonfixes isn't deactivated.

    Returns:
        bool: True, if the fix should be executed.

    """
    return (
        len(sys.argv) >= 1
        and 'STEAM_COMPAT_DATA_PATH' in os.environ
        and 'PROTONFIXES_DISABLE' not in os.environ
        and 'waitforexitandrun' in sys.argv[1]
    )


def check_iscriptevaluator() -> bool:
    """Determine, if we were invoked while running "iscriptevaluator.exe".

    Returns:
        bool: True, if we were invoked while running "iscriptevaluator.exe".

    """
    return len(sys.argv) >= 3 and 'iscriptevaluator.exe' in sys.argv[2]


def setup(
    env: dict,
    bin_path_var: str,
    lib_path_var: str,
    func: Callable[[dict, str, str, str], None],
) -> None:
    """Setup PATH and LD_LIBRARY_PATH to include protonfixes's binary and library paths"""
    func(env, bin_path_var, bin_dir, ':')
    func(env, lib_path_var, f'{x86_64_lib_dir}:{i386_lib_dir}', ':')


def execute() -> None:
    """Execute protonfixes"""
    if check_iscriptevaluator():
        log.debug('Skipping fix execution. We are running "iscriptevaluator.exe".')
    elif not check_conditions():
        log.warn('Skipping fix execution. We are probably running an unit test.')
    else:
        try:
            fix.main()

        # Catch any exceptions and print a traceback
        except Exception:
            sys.stderr.write('ProtonFixes ' + traceback.format_exc())
            sys.stderr.flush()


__all__ = ['setup', 'execute']
