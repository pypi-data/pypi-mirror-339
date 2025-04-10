import bisect
import math
import random
import string
from collections import Counter, defaultdict
from collections.abc import Iterator
from typing import Any

import numpy

from .channel import Channel


def generate_partition_id(publisher_id: str, channel: Channel | None = None) -> str:
    alphanum = string.ascii_uppercase + string.digits
    rand_id = "".join(random.SystemRandom().choice(alphanum) for _ in range(6))
    if channel:
        subsystem = channel.name.split(":")[1].split("-")[0]
        return f"{publisher_id}_{subsystem}_{rand_id}"
    else:
        return f"{publisher_id}_{rand_id}"


def grouped(items: list[Any], n: int) -> Iterator[list[Any]]:
    for i in range(0, len(items), n):
        yield items[i : i + n]


def partition_channels(
    channels: list[Channel],
    publisher: str,
    metadata: dict[str, Channel] | None = None,
    max_channels: int = 100,
    partition_fraction: float = 0.8,
) -> list[Channel]:
    """determine partitions IDs for channels

    Parameters
    ----------
    channels : list[Channel]
        List of channels for which to determine partition IDs
    publisher: str
        A publisher ID to apply to all channels being partitioned.
        This will override any publisher already specified in the
        channel metadata returned.
    metadata: dict[str, Channel]
        An existing channel metadata dictionary, from which existing
        partition information will be taken.
    max_channels: int
        The maximum number per partition.
    partition_fraction: float
        Fraction of max channels to use in intial partition
        allocation.

    Returns the initially provided channel list updated with publisher
    and partition info.

    """
    if not metadata:
        metadata = {}

    updated = {}

    # map channels to dtypes
    channels_by_dtype: dict[numpy.dtype | None, list[Channel]] = {}
    for channel in channels:
        channels_by_dtype.setdefault(channel.data_type, []).append(channel)

    # filter channels that aren't matched to an ID
    # handle each data type separately
    for subblock in channels_by_dtype.values():
        # filter channels that aren't matched to an ID
        subblock_group = {channel.name for channel in subblock}
        subpartitions = {
            name: meta.partition_id
            for name, meta in metadata.items()
            if name in subblock_group and meta.publisher == publisher
        }
        unmatched = [
            channel for channel in subblock if channel.name not in subpartitions
        ]
        part_count = Counter(subpartitions.values())
        ordered = sorted(list(subpartitions.keys()))

        # determine where channel would go in sorted order
        insert_pt = defaultdict(list)
        for channel in unmatched:
            idx = bisect.bisect_left(ordered, channel.name)
            insert_pt[idx].append(channel)

        # assign unmatched into existing or new partitions
        max_partition_size = math.floor(partition_fraction * max_channels)
        for idx, adjacent in insert_pt.items():
            insert_idx = min(idx, len(ordered) - 1)

            if insert_idx == -1:
                # no initial partitions
                partition_id = generate_partition_id(publisher, adjacent[0])
            else:
                id_ = metadata[ordered[insert_idx]].partition_id
                assert isinstance(id_, str)
                partition_id = id_

            if part_count[partition_id] + len(adjacent) > max_channels:
                # assign to new partition
                for group in grouped(adjacent, max_partition_size):
                    partition_id = generate_partition_id(publisher, group[0])
                    for channel in group:
                        updated[channel.name] = Channel(
                            channel.name,
                            data_type=channel.data_type,
                            sample_rate=channel.sample_rate,
                            publisher=publisher,
                            partition_id=partition_id,
                        )
                    part_count[partition_id] += len(group)
            else:
                # assign to existing partition
                for channel in adjacent:
                    updated[channel.name] = Channel(
                        channel.name,
                        data_type=channel.data_type,
                        sample_rate=channel.sample_rate,
                        publisher=publisher,
                        partition_id=partition_id,
                    )
                part_count[partition_id] += len(adjacent)

    # fill in any channels that were not newly partitioned
    for channel in channels:
        if channel.name in updated:
            continue
        assert metadata[channel.name].partition_id
        updated[channel.name] = Channel(
            channel.name,
            data_type=channel.data_type,
            sample_rate=channel.sample_rate,
            publisher=publisher,
            partition_id=metadata[channel.name].partition_id,
        )

    # return same channel list order as passed in
    return [updated[channel.name] for channel in channels]
