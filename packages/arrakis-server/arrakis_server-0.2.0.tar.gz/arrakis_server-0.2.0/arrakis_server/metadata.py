# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Protocol

import numpy
import toml

from .channel import Channel
from .partition import partition_channels

logger = logging.getLogger("arrakis")


class ChannelMetadataBackend(Protocol):
    def update(self, channels: Iterable[Channel]) -> None:
        """Update channel metadata.

        Parameters
        ----------
        channels : Iterable[Channel]
            Channels for which to update metadata with.

        """
        ...

    def load(cls, *args, **kwargs) -> list[Channel]:
        """Load channel metadata"""
        ...

    def find(
        self,
        *,
        pattern: str,
        data_type: list[str],
        min_rate: int,
        max_rate: int,
        publisher: list[str],
    ) -> Iterable[Channel]:
        """Find channels matching a set of conditions.

        Parameters
        ----------
        pattern : str
            Channel pattern to match channels with, using regular expressions.
        data_type : list[str]
            Data types to match.
        min_rate : int
            Minimum sampling rate for channels.
        max_rate : int
            Maximum sampling rate for channels.
        publisher : list[str]
            Publishers to match.

        Returns
        -------
        Iterable[Channel]
            Channel objects for all channels matching query.

        """
        ...

    def describe(self, *, channels: Iterable[str]) -> Iterable[Channel]:
        """Get channel metadata for channels requested.

        Parameters
        ----------
        channels : Iterable[str]
            Channels to request.

        Returns
        -------
        Channel
            Channel objects, one per channel requested.

        """
        ...


class ChannelConfigBackend(ChannelMetadataBackend):
    """A channel metadata backend backed by configuration.

    Channel metadata is stored as a configuration file in the TOML format.

    """

    def __init__(
        self,
        cache_file: Path | None = None,
        enforce: Iterable[str] | None = None,
    ):
        """initialize backend

        Parameters
        ----------
        cache_file : Path, optional
            Path to file that will hold channel metadata for
            publishers that are publishing their own channel lists.
        enforce : list[str], optional
            A list of Channel properties to enforce the presence of.

        """
        self.cache_file = cache_file
        # always enforced parameters
        self.enforce = {"sample_rate", "data_type"}
        if enforce:
            self.enforce |= set(enforce)

        self.metadata: dict[str, Channel] = {}
        self.extra: dict[str, dict[str, Any]] = {}
        # used for tracking if channels have been updated
        self._updated: dict[str, bool] = {}

        if self.cache_file is not None and self.cache_file.exists():
            self.load(self.cache_file)
            # reset the load tracking after loading the cache
            self._updated = {}

    def validate(self, channel: Channel) -> None:
        """return True if channel contains all enforced properties

        Raises a ValueError if the enforced properties are not present
        or None.

        """
        for prop in self.enforce:
            if not hasattr(channel, prop) or not getattr(channel, prop):
                raise ValueError(f"channel '{channel.name}' missing property {prop}")

    def update(self, channels: Iterable[Channel], overwrite: bool = False):
        """Update channel metadata and sync to cache

        Channels will be validated according to the enforced property
        list.

        Parameters
        ----------
        channels : list[Channel]
            List of channels to upate.
        overwrite : bool
            Whether to allow overwriting existing channels or not
            (default: False)

        """
        # update in-memory channel map
        for channel in channels:
            if not overwrite and self._updated.get(channel.name, False):
                raise ValueError(
                    f"attempt to overwrite existing channel: {channel.name}"
                )
            self.validate(channel)
            self.metadata[channel.name] = channel
            self._updated[channel.name] = True

        if not self.cache_file:
            return

        # write updated channel map to disk
        metadata = {}
        for name, meta in self.metadata.items():
            metadata[name] = {
                "sample_rate": meta.sample_rate,
                "data_type": numpy.dtype(meta.data_type).name,
                "partition_id": meta.partition_id,
                "publisher": meta.publisher,
            }
            if self.extra and name in self.extra:
                metadata[name].update(self.extra[name])

        with self.cache_file.open("w") as f:
            toml.dump(metadata, f)

    def load(
        self,
        path: Path,
        publisher: str | None = None,
        overwrite: bool = False,
    ) -> list[Channel]:
        """Load channel metadata from TOML file.

        If a publisher is specified this will also handle assigning
        Kafka partition IDs to the loaded channels.
        Returns the list of Channel objects loaded from the file.

        Parameters
        ----------
        path : Path
            Path to channel metadata toml file.
        publisher : str
            Publisher ID to apply to all channels being loaded from
            this file.
        overwrite : bool
            Whether to allow overwriting existing channels or not
            (default: False)

        Returns
        -------
        List[Channel]
            List of channels loaded from file.

        """
        logger.info("loading channel description file: %s", path)
        with path.open("r") as f:
            metadata = toml.load(f)

        channels = []
        extra = {}
        for name, meta in metadata.items():
            try:
                sample_rate = meta.pop("sample_rate")
            except KeyError:
                sample_rate = meta.pop("rate")
            try:
                data_type = numpy.dtype(meta.pop("data_type"))
            except KeyError:
                data_type = numpy.dtype(meta.pop("dtype"))
            channel = Channel(
                name,
                data_type=data_type,
                sample_rate=sample_rate,
                publisher=meta.pop("publisher", None),
                partition_id=meta.pop("partition_id", None),
            )
            channels.append(channel)
            extra[name] = meta

        if publisher is not None:
            channels = partition_channels(
                channels,
                metadata=self.metadata,
                publisher=publisher,
            )

        self.update(channels, overwrite=overwrite)
        self.extra.update(extra)

        return channels

    @property
    def scopes(self) -> dict[str, list[dict[str, Any]]]:
        """The scopes that the set of channels span."""
        scopes: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for channel in self.metadata.values():
            scopes[channel.domain].append({"subsystem": channel.subsystem})
        return scopes

    def find(
        self,
        *,
        pattern: str,
        data_type: list[str],
        min_rate: int,
        max_rate: int,
        publisher: list[str],
    ) -> Iterable[Channel]:
        expr = re.compile(pattern)
        channels = []
        dtypes = {numpy.dtype(dtype) for dtype in data_type}
        publishers = set(publisher)
        for channel in self.metadata.values():
            if expr.match(channel.name):
                rate = channel.sample_rate
                if not (rate >= min_rate and rate <= max_rate):
                    continue
                if dtypes and channel.data_type not in dtypes:
                    continue
                if publishers and channel.publisher not in publishers:
                    continue
                channels.append(channel)

        return channels

    def describe(self, *, channels: Iterable[str]) -> Iterable[Channel]:
        return [self.metadata[channel] for channel in channels]
