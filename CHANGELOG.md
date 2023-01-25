# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Supports short id that only 6 more letters for every methods such as `db['kcbPuq']`, not like `db['kcbPuqpfV3....'`. [(#6)](https://github.com/joonas-yoon/json-as-db/issues/6)

Thanks for getting this release out! please stay tuned :)

## [0.2.4]

### Added

- Supports to find by key and value with `Condition` that is generated from `Key`. [(#8)](https://github.com/joonas-yoon/json-as-db/issues/8)
- Implements useful representation for quickly displaying as a table format. [(#4)](https://github.com/joonas-yoon/json-as-db/issues/4)
- Add static method to load - `json_as_db.load(path)` [(#7)](https://github.com/joonas-yoon/json-as-db/issues/7)
- Add a variable `__version__` in global.

### Fixed

- Implements `items()` methods to override dictionary on `Database` class. [(#3)](https://github.com/joonas-yoon/json-as-db/issues/3)
- Getter supports list-like parameter such as `db[['id1', 'id2']]` [(#5)](https://github.com/joonas-yoon/json-as-db/issues/5)

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
[0.2.4]: https://github.com/joonas-yoon/json-as-db/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/joonas-yoon/json-as-db/compare/v0.2.0...v0.2.3
[0.2.2]: https://github.com/joonas-yoon/json-as-db/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/joonas-yoon/json-as-db/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/joonas-yoon/json-as-db/releases/tag/v0.1.0
