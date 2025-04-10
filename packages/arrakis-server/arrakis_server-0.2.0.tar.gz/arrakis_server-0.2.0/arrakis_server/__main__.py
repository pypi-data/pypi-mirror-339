import argparse
import logging
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor, wait

from . import __version__
from .backends import BackendType
from .constants import DEFAULT_LOCATION
from .scope import ScopeMap
from .server import ArrakisFlightServer

logger = logging.getLogger("arrakis")


def get_log_level(args: argparse.Namespace) -> int:
    """Determine the log level from logging options."""
    if args.quiet:
        return logging.WARNING
    elif args.verbose:
        return logging.DEBUG
    else:
        return logging.INFO


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="arrakis-server",
        description="Arrakis Arrow Flight server.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="terse logging, show only warnings and errors",
    )
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose logging",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        default=DEFAULT_LOCATION,
        help=(
            f"serve requests at this URL, default: {DEFAULT_LOCATION}."
            "  specify '0' to pick a random port on localhost"
        ),
    )
    parser.add_argument(
        "-s",
        "--scope-map-file",
        "--scope-map",
        type=pathlib.Path,
        metavar="SCOPE.yaml",
        help="scope map YAML file",
    )

    # backend subparsers
    subparsers = parser.add_subparsers(
        title="Backends",
        description="""Backends determine how to access the data to be
        served to clients.  Each backend defines its own arguments,
        see \"<BACKEND NAME> -h\" for more info.  If a backend is not
        specified then the server will act as an information server
        only.""",
        metavar="Available backends:",
        dest="backend",
    )
    for _backend in BackendType:
        if _backend.value is None:
            continue
        bparser = subparsers.add_parser(
            _backend.name,
            aliases=[_backend.name.lower()],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            help=_backend.value.__doc__.splitlines()[0],
            description=_backend.value.__doc__,
        )
        bparser.set_defaults(backend=_backend)
        _backend.value.add_arguments(bparser)

    # parse command line args
    args = parser.parse_args()

    # set up logger
    logger = logging.getLogger("arrakis")
    log_level = get_log_level(args)
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s | arrakis : %(levelname)s : %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    ##############################

    logger.info("Arrakis server %s", __version__)

    # load scope map
    scope_map = None
    if args.scope_map_file:
        logger.info("loading global scope map %s", args.scope_map_file)
        scope_map = ScopeMap.load(args.scope_map_file)
        for loc, info in scope_map.servers.items():
            logger.info("  %s: %s", loc, info.domains)
    else:
        logger.info("no scope map specified.")

    # initialize the backend
    if args.backend:
        logger.info("initializing %s backend...", args.backend.name)
        backend = args.backend.value.from_args(args)
    else:
        logger.info("no backend specified.")
        if not args.scope_map_file:
            parser.exit(
                1, "error: Nothing to serve, must specify scope map and/or backend.\n"
            )
        backend = None

    # serve requests
    logger.info("initializing Flight server...")
    server = ArrakisFlightServer(
        url=args.url,
        backend=backend,
        scope_map=scope_map,
    )
    logger.info("Flight server initialized")

    # serve requests
    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            future = executor.submit(_run_until_shutdown, server)
            wait([future])
        except KeyboardInterrupt:
            server.shutdown()


def _run_until_shutdown(server: ArrakisFlightServer) -> None:
    """Run an Arrakis server instance until a shutdown request is received."""
    logger.info("serving...")
    with server:
        server.wait_until_shutdown()


if __name__ == "__main__":
    main()
