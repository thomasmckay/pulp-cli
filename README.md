# pulp-cli

This is a proof-of-concept intended to demonstrate an auto-generated Pulp 3 CLI.

## Demo

![Demo pic](https://i.imgur.com/AsgaO1Q.png)

## Features

- Auto-generated CLI commands with one command for each API endpoint
- Support for plugins
- Pagination support
- Lookup via resource IDs or names
- Help screens
- Task polling
- Autocompletion for commands and arguements
- Extensibility
  - Support in the future to create our own complex commands/workflows
  - Users/plugin writers can create their own commands and ship their own cli plugins

## Installation

```
$ git clone -b click https://github.com/werwty/pulp-cli.git && cd pulp-cli
$ mkvirtualenv --python="/usr/bin/python3" pulp-cli
$ pip install -e .
$ mkdir ~/.coreapi
$ http :8000/pulp/api/v3/?format=corejson > ~/.coreapi/document.json
```

## Autocompletion

To install autocompletion, simply run:

```
pulp --install bash
```

## Basic Usage

To create a repository:

```
$ pulp repositories create --name foo
```

At any time, see a command's help screen:

```
$ pulp repositories create --help
```

Or simply view a command's subcommands:

```
$ pulp repositories
```
