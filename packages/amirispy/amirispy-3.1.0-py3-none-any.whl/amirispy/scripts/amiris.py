#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

from typing import Optional, List

from amirispy.scripts.subcommands.batch import batch_run_amiris
from amirispy.scripts.subcommands.compare import compare_results
from amirispy.scripts.subcommands.download import download_amiris
from amirispy.scripts.subcommands.run import run_amiris
from amirispy.source.cli import (
    arg_handling_run,
    Command,
    CompareOptions,
    DownloadOptions,
    RunOptions,
    BatchOptions,
    GeneralOptions,
    CommandLineError,
)
from amirispy.source.logs import set_up_logger, log_and_print


def amiris_cli(args: Optional[List[str]] = None) -> None:
    """Calls sub-commands with appropriate arguments as returned by the command line parser"""
    try:
        command, options = arg_handling_run(args)
    except CommandLineError as e:
        raise SystemExit(e)

    set_up_logger(options[GeneralOptions.LOG], options[GeneralOptions.LOGFILE])
    if command is Command.DOWNLOAD:
        log_and_print("Starting install script")
        download_amiris(
            options[DownloadOptions.URL],
            options[DownloadOptions.TARGET],
            options[DownloadOptions.FORCE],
            options[DownloadOptions.MODE],
        )
        log_and_print(f"Installation setup to '{options[DownloadOptions.TARGET]}' complete")
    elif command is Command.RUN:
        log_and_print("Start running AMIRIS")
        run_amiris(options)
        log_and_print(f"Successfully executed AMIRIS. See your results in '{options[RunOptions.OUTPUT]}'")
    elif command is Command.BATCH:
        log_and_print("Start running AMIRIS batch run")
        batch_run_amiris(options)
        log_and_print(f"Successfully executed AMIRIS. See your results in '{options[BatchOptions.OUTPUT]}'")
    elif command is Command.COMPARE:
        log_and_print("Starting comparison script")
        compare_results(options[CompareOptions.EXPECTED], options[CompareOptions.TEST], options[CompareOptions.IGNORE])


if __name__ == "__main__":
    amiris_cli()
