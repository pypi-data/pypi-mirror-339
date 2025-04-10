# Changelog

## [Unreleased]

## [0.2.0] - 2025-04-09

### Added

- Add ability to assign a random port for server

### Fixed

- Better endpoint handling for endpoint construction
- Raise import errors when loading backend plugins from entrypoints
- Allow server to stop in-process stream requests prior to shutdown

### Changed

- CLI: handle backends as 'subcommands', i.e. arrakis-server KAFKA, rather than
  via --backend KAFKA. This allows backends to specify their own server command
  line arguments
- Change name of ConfigMetadataBackend to ChannelConfigBackend, simplify
  interface
- Rework ChannelConfigBackend to enforce channel properties, protect against
  overwriting channels
- partition: rework `partition_channels`:
  * Don't update metadata in place
  * Assign publisher ID to channels
  * Ensure all channels are returned in the same order
  * Tweak partition naming scheme (remove domain, rely on publisher ID)
- metadata: handle partitioning within the load method
- metadata: Fix check for cache file when initializing

## [0.1.0] - 2025-03-13

- Initial release

[unreleased]: https://git.ligo.org/ngdd/arrakis-server/-/compare/0.2.0...main
[0.2.0]: https://git.ligo.org/ngdd/arrakis-server/-/tags/0.2.0
[0.1.0]: https://git.ligo.org/ngdd/arrakis-server/-/tags/0.1.0
