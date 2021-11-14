# figfind

### Find and save the path to your config files!

## Installation

Install poetry for a python package manager. Then use it to install your virtual environment

```
$ poetry install
```

Enter the virtual environment (and leave it when finished).

```bash
$ poetry shell
```

Set up pre-commit:

```sh
$ pre-commit install
$ pre-commit run --all-files
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### run pytest / coverage

$ make test
```
