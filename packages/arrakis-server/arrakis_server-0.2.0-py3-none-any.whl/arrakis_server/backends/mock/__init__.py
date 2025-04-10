# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

from __future__ import annotations

import argparse
import logging
import time
from collections.abc import Callable, Iterable, Iterator
from importlib import resources
from pathlib import Path
from typing import TypeAlias

import gpstime
import numpy
import pyarrow
from arrakis import SeriesBlock, Time
from pyarrow import flight
from sympy import lambdify, parse_expr
from sympy.abc import t

from ...channel import Channel
from ...metadata import ChannelConfigBackend
from ...scope import Retention, ScopeInfo
from ...traits import ServerBackend
from . import channels as channel_lists

logger = logging.getLogger("arrakis")


ArrayTransform: TypeAlias = Callable[[numpy.ndarray], numpy.ndarray]


def _func_random_normal(t):
    return numpy.random.normal(size=len(t))


def load_channel_funcs(metadata: ChannelConfigBackend) -> dict[str, ArrayTransform]:
    """load channel description TOML files

    Returns a dictionary of channel: channel_obj.

    Channels should be defined in tables, with the channel name in the
    header.  The table should include:

      `rate`  in samples per second
      `dtype` as a python dtype
      `func`  an optional function to generate the data, will be given
              the block time array as it's single argument. any sympy
              expression containing the t variable is valid
              (numpy.random.uniform used by default)

    example:

    ["MY:CHANNEL-NAME"]
    rate = 16384
    dtype = "float32"
    func = "3*t + cos(t)"

    """
    channel_func_map = {}
    for channel_name, meta in metadata.extra.items():
        if "func" in meta:
            expr = parse_expr(meta["func"])
            func = lambdify(t, expr, "numpy")
        else:
            func = _func_random_normal
        channel_func_map[channel_name] = func
    return channel_func_map


class MockBackend(ServerBackend):
    """Mock server backend that generates synthetic timeseries data.

    If channel definition files are not provided then the Mock backend
    will serve a pre-defined set of H1: and L1: channels.

    """

    def __init__(self, channel_files: list[Path] | None = None):
        """Initialize mock server with list of channel definition files."""
        if not channel_files:
            with (
                resources.as_file(
                    resources.files(channel_lists).joinpath("H1_channels.toml")
                ) as H1_file,
                resources.as_file(
                    resources.files(channel_lists).joinpath("L1_channels.toml")
                ) as L1_file,
            ):
                channel_files = [H1_file, L1_file]
        self.metadata = ChannelConfigBackend()
        for channel_file in channel_files:
            self.metadata.load(channel_file)
        self._channel_func_map = load_channel_funcs(self.metadata)

        self.scope_info = ScopeInfo(self.metadata.scopes, Retention())

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser):
        """add arguments for this backend to an argparse subparser"""
        parser.add_argument(
            "channel_files",
            metavar="CHANNELS.toml",
            nargs="*",
            type=Path,
            help="Channel definition TOML file (may be specified multiple times).",
        )

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> MockBackend:
        """initialize class from argparse namespace"""
        return cls(args.channel_files)

    def find(
        self,
        *,
        pattern: str,
        data_type: list[str],
        min_rate: int,
        max_rate: int,
        publisher: list[str],
    ) -> Iterable[Channel]:
        assert isinstance(self.metadata, ChannelConfigBackend)
        return self.metadata.find(
            pattern=pattern,
            data_type=data_type,
            min_rate=min_rate,
            max_rate=max_rate,
            publisher=publisher,
        )

    def describe(self, *, channels: Iterable[str]) -> Iterable[Channel]:
        self._check_channels(channels)
        assert isinstance(self.metadata, ChannelConfigBackend)
        return self.metadata.describe(channels=channels)

    def stream(
        self, *, channels: Iterable[str], start: int, end: int
    ) -> Iterator[SeriesBlock]:
        self._check_channels(channels)
        return self._generate_series(channels, start, end)

    def _check_channels(self, channels: Iterable[str]):
        bad_channels = [
            channel for channel in channels if channel not in self.metadata.metadata
        ]
        if bad_channels:
            # FIXME: is this the correct error to return?
            raise flight.FlightServerError(
                f"the following channels are not available on this server: {bad_channels}"  # noqa E501
            )

    def _generate_block(self, channels: Iterable[str], timestamp: int) -> SeriesBlock:
        assert isinstance(self.metadata, ChannelConfigBackend)
        channel_data = {}
        channel_dict = {}
        for channel in channels:
            metadata = self.metadata.metadata[channel]
            rate = metadata.sample_rate
            assert rate is not None
            size = rate // 16
            dtype = metadata.data_type
            time_array = timestamp + numpy.arange(size) / rate
            func = self._channel_func_map[channel]
            data = numpy.array(
                numpy.broadcast_to(func(time_array), time_array.shape),
                dtype=dtype,
            )
            channel_data[channel] = data
            channel_dict[channel] = metadata

        return SeriesBlock(timestamp, channel_data, channel_dict)

    def _generate_series(
        self,
        channels: Iterable[str],
        start: int | None,
        end: int | None,
    ) -> Iterator[SeriesBlock]:
        dt = Time.SECONDS // 16

        if start:
            current = start
        else:
            current = (int(gpstime.gpsnow() * Time.SECONDS) // dt) * dt

        def _run(current: int):
            if end:
                return current < end
            return True

        while _run(current):
            yield self._generate_block(channels, current)
            current += dt
            now = int(gpstime.gpsnow() * Time.SECONDS)
            if current >= now:
                # sleep for up to dt to simulate live stream
                time.sleep(max((current - now) / Time.SECONDS, 0))
