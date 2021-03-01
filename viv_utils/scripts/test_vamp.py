import sys
import time
import logging
import argparse
import contextlib

from viv_utils import getWorkspace, is_library_function


logger = logging.getLogger(__name__)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    desc = ""
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "sample",
        type=str,
        help="path to sample to analyze",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debugging output on STDERR"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="disable all output but errors"
    )
    args = parser.parse_args(args=argv)

    if args.quiet:
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger().setLevel(logging.WARNING)
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)

    with timing("creating workspace"):
        vw = getWorkspace(args.sample, should_save=False)

    thunks = libs = regular = 0
    for va in sorted(vw.getFunctions()):
        if vw.isFunctionThunk(va):
            thunks += 1
        elif is_library_function(vw, va):
            libs += 1
        else:
            regular += 1
    print("libs:    %4d\nthunks:  %4d\nregular: %4d" % (libs, thunks, regular))


@contextlib.contextmanager
def timing(msg):
    t0 = time.time()
    yield
    t1 = time.time()
    logger.debug("perf: %s: %0.2fs", msg, t1 - t0)


if __name__ == "__main__":
    sys.exit(main())
