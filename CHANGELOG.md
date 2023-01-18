# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Thanks for getting this release out! please stay tuned :)

## [0.2.3] - 2023-01-18

### Added

- Supports to load database from JSON file that doesn't made from `Database`.

## [0.2.2] - 2022-12-26

### Added

- Unit tests for getters.
- `Database` read items from serialized JSON file.

### Changed

- Remove `Client`. use methods on `Database` instead of.

## [0.1.1] - 2022-12-26

### Added

- Documentation and comments.
- Implements `len` method on `Database`.

### Fixed

- apply style format based on PEP8

### Changed

- Remove async/await keyword from `Database`.
- `Database.modify()` returns modified value(s)

## [0.1.0] - 2022-12-22

This is the very first version of package.

Also this is not stable, so under alpha-test.

### Major changes

- Set up files to being python package
- Organized direcotries

[Unreleased]: https://github.com/joonas-yoon/json-as-db/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/joonas-yoon/json-as-db/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/joonas-yoon/json-as-db/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/joonas-yoon/json-as-db/releases/tag/v0.1.0
