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
$ git clone https://github.com/werwty/pulp-cli.git && cd pulp-cli
$ mkvirtualenv --python="/usr/bin/python3" pulp-cli
$ pip install -e .
```

## Load Pulp COREAPI Schema

The Pulp API schema has to be loaded before the CLI can be used

```
pulp get --url=http://pulp3.dev:8000/pulp/api/v3/?format=corejson
```

## Set up autocompletion

Run this command in your preferred shell. Currently supports bash, zsh, fish, and powershell

```
$ pulp --autocomplete
```

## Example Usage

At any time, see a command's help screen:

```
$ pulp repositories create --help
```

### Create a repository

```
$ pulp repositories create --name=foo
{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/",
    "_latest_version_href": null,
    "_versions_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/",
    "created": "2018-06-08T19:21:48.193530Z",
    "description": "",
    "id": "c3550bb7-1984-4bd4-bbc4-5bc5483008b5",
    "name": "foo",
    "notes": {}
}
```

### List repositories

```
$ pulp repositories list
{
    "next": null,
    "previous": null,
    "results": [
        {
            "_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/",
            "_latest_version_href": null,
            "_versions_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/",
            "created": "2018-06-08T19:21:48.193530Z",
            "description": "",
            "id": "c3550bb7-1984-4bd4-bbc4-5bc5483008b5",
            "name": "foo",
            "notes": {}
        }
    ]
}
```

### Create a remote
```
$ pulp remotes file create --name=bar --url=https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST
{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/remotes/file/396b7eb5-97aa-4394-bc25-ca8be7dd19c4/",
    "created": "2018-06-08T19:24:02.416156Z",
    "id": "396b7eb5-97aa-4394-bc25-ca8be7dd19c4",
    "last_synced": null,
    "last_updated": "2018-06-08T19:24:02.416180Z",
    "name": "bar",
    "proxy_url": "",
    "ssl_validation": true,
    "type": "file",
    "url": "https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST",
    "validate": true
}

```

### Sync Repository foo with Remote bar

```
$ pulp remotes file sync --repository=http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/ --id=396b7eb5-97aa-4394-bc25-ca8be7dd19c4
{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/tasks/97ba7d54-4168-4895-942c-4b45c1b20a48/",
    "task_id": "97ba7d54-4168-4895-942c-4b45c1b20a48"
}

Loading -{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/tasks/97ba7d54-4168-4895-942c-4b45c1b20a48/",
    "created": "2018-06-08T19:32:22.081480Z",
    "created_resources": [
        "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/1/"
    ],
    "error": null,
    "finished_at": "2018-06-08T19:32:23.307490Z",
    "id": "97ba7d54-4168-4895-942c-4b45c1b20a48",
    "non_fatal_errors": [],
    "parent": null,
    "progress_reports": [
        {
            "done": 3,
            "message": "Add Content",
            "state": "completed",
            "suffix": "",
            "task": "http://pulp3.dev:8000/pulp/api/v3/tasks/97ba7d54-4168-4895-942c-4b45c1b20a48/",
            "total": 3
        },
        {
            "done": 0,
            "message": "Remove Content",
            "state": "completed",
            "suffix": "",
            "task": "http://pulp3.dev:8000/pulp/api/v3/tasks/97ba7d54-4168-4895-942c-4b45c1b20a48/",
            "total": 0
        }
    ],
    "spawned_tasks": [],
    "started_at": "2018-06-08T19:32:22.175157Z",
    "state": "completed",
    "worker": "http://pulp3.dev:8000/pulp/api/v3/workers/41f6d8b8-1a94-4338-8f0a-7234d3ee6760/"
}

```

### View all repository version
```
$ pulp repositories versions list
Repository pk: foo
{
    "next": null,
    "previous": null,
    "results": [
        {
            "_added_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/1/added_content/",
            "_content_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/1/content/",
            "_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/1/",
            "_removed_href": "http://pulp3.dev:8000/pulp/api/v3/repositories/c3550bb7-1984-4bd4-bbc4-5bc5483008b5/versions/1/removed_content/",
            "content_summary": {
                "file": 3
            },
            "created": "2018-06-08T19:32:22.203681Z",
            "id": "10fd997a-bd96-4f5d-9df7-42939ed46343",
            "number": 1
        }
    ]
}
```

### Create a Publisher
```
$ pulp publishers file create
Name: bar
{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/publishers/file/5eb270e4-88e6-4952-aba0-02983f784293/",
    "created": "2018-06-10T23:52:45.045851Z",
    "distributions": [],
    "id": "5eb270e4-88e6-4952-aba0-02983f784293",
    "last_published": null,
    "last_updated": "2018-06-10T23:52:45.045869Z",
    "name": "bar",
    "type": "file"
}
```

### Use the bar Publisher to create a Publication
```
$ pulp publishers file publish --id=5eb270e4-88e6-4952-aba0-02983f784293 --repository=http://pulp3.dev:8000/pulp/api/v3/repositories/90fa0c62-4d35-4a3b-99b7-d1b1a2c9c01e/
{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/tasks/5078d4c4-a152-4ac9-8b3a-e0d1c5c62e28/",
    "task_id": "5078d4c4-a152-4ac9-8b3a-e0d1c5c62e28"
}

Loading |{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/tasks/5078d4c4-a152-4ac9-8b3a-e0d1c5c62e28/",
    "created": "2018-06-11T00:33:58.785480Z",
    "created_resources": [
        "http://pulp3.dev:8000/pulp/api/v3/publications/20e44b38-e3d2-455f-af1a-d8aa3e720851/"
    ],
    "error": null,
    "finished_at": "2018-06-11T00:33:58.985735Z",
    "id": "5078d4c4-a152-4ac9-8b3a-e0d1c5c62e28",
    "non_fatal_errors": [],
    "parent": null,
    "progress_reports": [],
    "spawned_tasks": [],
    "started_at": "2018-06-11T00:33:58.899002Z",
    "state": "completed",
    "worker": "http://pulp3.dev:8000/pulp/api/v3/workers/fb1e6a46-c463-4d2d-b684-04c47da827c3/"
}
```
### Create a Distribution for the Publication
```
$ pulp distributions create --name=baz --base_path=foo --publication=http://pulp3.dev:8000/pulp/api/v3/publications/20e44b38-e3d2-455f-af1a-d8aa3e720851/
{
    "_href": "http://pulp3.dev:8000/pulp/api/v3/distributions/1c30053e-4921-4ad7-ac18-cb68150df4fa/",
    "base_path": "foo",
    "base_url": "pulp3.dev:8000/pulp/content/foo",
    "created": "2018-06-11T00:38:09.543133Z",
    "id": "1c30053e-4921-4ad7-ac18-cb68150df4fa",
    "name": "baz",
    "publication": "http://pulp3.dev:8000/pulp/api/v3/publications/20e44b38-e3d2-455f-af1a-d8aa3e720851/",
    "publisher": null,
    "repository": null
}
```
