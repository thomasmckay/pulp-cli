# Installation

1. `git clone git@github.com:werwty/pulpcli-POC.git`
2. `pip3 install -e pulpcli-POC`


# Download document.json

This currently needs to be saved to /home/vagrant/.coreapi/documents.json, support
for storing it at a non hardcoded position is incoming

```
$ wget http://pulp3.dev:8000/pulp/api/v3/?format=corejson
```


# Set up BASH Completion

```
$ pulp --install bash
```


# Example Usage

## Create a repository

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

## List repositories

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

## Create a remote
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

## Sync Repository foo with Remote bar

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

## View all repository version
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