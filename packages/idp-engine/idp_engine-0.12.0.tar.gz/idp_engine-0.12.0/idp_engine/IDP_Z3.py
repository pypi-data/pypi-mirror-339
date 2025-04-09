# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle

# This file is part of IDP-Z3.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""

The command-line program to execute an IDP file with a main() block.

"""

import argparse
import os
import sys
import time

from idp_engine import IDP
from z3 import set_option
from idp_engine.utils import PROCESS_TIMINGS


def cli(args=None):
    parser = argparse.ArgumentParser(description="IDP-Z3")
    parser.add_argument("--version", "-v", action="version", version="0.12.0")
    parser.add_argument("FILE", help="path to the .idp file", type=str)
    parser.add_argument("-o", "--output", help="name of the output file", type=str)
    parser.add_argument(
        "--full-formula",
        help="show the full formula",
        dest="formula",
        action="store_true",
    )
    parser.add_argument(
        "--no-timing",
        help="don't display timing information",
        dest="timing",
        action="store_false",
        default=True,
    )
    args = parser.parse_args()
    error = 0

    if args.formula:
        set_option(
            max_args=10000000,
            max_lines=1000000,
            max_depth=10000000,
            max_visited=1000000,
        )

    start_time = time.time()
    if args.FILE:
        dir = os.getcwd()
        file = os.path.join(dir, args.FILE)
        with open(file, "r", encoding="utf-8") as f:
            theory = f.read()

        parse_start = time.time()
        idp = IDP.from_str(theory)
        PROCESS_TIMINGS["parse"] = time.time() - parse_start
        if not args.output:
            # Print output to stdout.
            PROCESS_TIMINGS["ground"] = time.time()
            print(idp.execute(capture_print=True))
        else:
            # Print output to file.
            out = []  # list of printed lines
            try:
                prints = idp.execute(capture_print=True)
                if prints is not None:
                    out.append(prints[: -len(os.linesep)])
            except Exception as exc:
                out.append(str(exc))
                error = 1
            with open(args.output, "w", encoding="utf-8") as f:
                for line in out:
                    f.write(line)
                    f.write(os.linesep)
        if args.timing:
            print(
                f"Elapsed time: {round(time.time() - start_time, 4)}s"
                f" (Parse: {round(PROCESS_TIMINGS['parse'], 4)}s"
                f" | Ground: {round(PROCESS_TIMINGS['ground'], 4)}s"
                f" | Solve: {round(PROCESS_TIMINGS['solve'], 4)}s)"
            )
    else:
        parser.print_help()

    sys.exit(error)


if __name__ == "__main__":
    cli()
