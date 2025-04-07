# Contributing to Claudebook

Thanks for your interest in contributing to Claudebook! 

## Getting Started

This project uses `uv` (and optionally, `npm` for formatting markdown).

- Installing `uv`: https://docs.astral.sh/uv/getting-started/installation/
- Installing `npm`: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

## Development

All development tasks are handled by `lefthook`, which is also used as a pre-commit hook.

```
uv run lefthook install
```

See https://lefthook.dev/ for more info.

### Common tasks

- Run all checks: `uv run lefthook pre-commit --all-files
- Run tests: `uv run pytest`

## Release

TODO

## Code of Conduct

Please be respectful and considerate of others when contributing.