import click
import click_completion
import coreapi
import json
import os
import requests
import urllib.parse as urlparse

from progress.spinner import Spinner
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter
from time import sleep
from uuid import UUID

CLI_PATH = os.path.join(os.path.expanduser("~"), ".pulpcli")
DOCUMENT_PATH = os.path.join(CLI_PATH, "document.json")

click_completion.init()
decoded_doc = None
coreapi_client = coreapi.Client()


def get_document():
    if not os.path.exists(DOCUMENT_PATH):
        click.echo("No schema set. Please use pulp get --url to set the schema")
        return None
    store = open(DOCUMENT_PATH, "rb")
    content = store.read()
    store.close()
    codec = coreapi.codecs.CoreJSONCodec()
    return codec.decode(content)


def get_raw_document():
    if not os.path.exists(DOCUMENT_PATH):
        return {}
    with open(DOCUMENT_PATH, "r") as doc:
        return json.load(doc)


# Install for click-completion
def autocomplete_callback(ctx, attr, value):
    if not value or ctx.resilient_parsing:
        return value
    shell, path = click_completion.install()
    click.echo("{} completion installed in {}".format(shell, path))
    exit(0)


@click.group(invoke_without_command=True)
@click.option(
    "--autocomplete",
    is_flag=True,
    callback=autocomplete_callback,
    expose_value=False,
    help="Install autocompletion for the current shell. Supported shells: bash, zsh, fish, powershell",
)
@click.pass_context
def client(ctx):
    if ctx.invoked_subcommand is not None:
        return
    click.echo(ctx.get_help())


@client.command(help="Fetch a coreapi schema")
@click.option("--url", help="url to pulp coreapi schema")
def get(url):
    if not os.path.exists(CLI_PATH):
        os.mkdir(CLI_PATH)
    resp = requests.get(url)
    open(DOCUMENT_PATH, "wb").write(resp.content)
    click.echo("Schema written to {}".format(DOCUMENT_PATH))
    exit(0)

def is_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True


def echo_resp(response):
    try:
        body = json.dumps(obj=response, sort_keys=True, ensure_ascii=False, indent=4)
    except ValueError:
        codec = coreapi.codecs.DisplayCodec()
        click.secho(codec.encode(response, colorize=True), fg="green")
    else:
        click.echo(highlight(body, JsonLexer(), Terminal256Formatter()))


def apicall(*args, **kwargs):

    ctx = click.get_current_context()
    keys = ctx.command_path.split(" ")[1:]

    params = {k: v for k, v in kwargs.items() if v is not None}

    for k, v in params.items():

        # If as passed in pk is not a uuid, see if we can find the uuid
        if (k.endswith("_pk") or k == "id") and not is_uuid4(v):
            resp = coreapi_client.action(
                get_document(), [keys[0], "list"], params={"name": v}
            )
            if len(resp["results"]) == 1:
                params[k] = resp["results"][0]["id"]
            else:
                click.secho("Invalid id or name", fg="red")
                return

    resp = coreapi_client.action(get_document(), keys, params=params)

    echo_resp(resp)

    # If coreapi client returns task_id, follow it and run a spinner until task is complete
    if resp and "task_id" in resp:
        spinner = Spinner("Loading ")
        task_progress = coreapi_client.action(
            get_document(), ["tasks", "read"], params={"id": resp.get("task_id")}
        )
        while task_progress["state"] != "completed":
            spinner.next()
            sleep(.01)
            task_progress = coreapi_client.action(
                get_document(), ["tasks", "read"], params={"id": resp.get("task_id")}
            )
        echo_resp(task_progress)

    # Pagination support
    while resp.get("next") or resp.get("previous"):
        move = click.prompt("N for next page, P for previous")
        if move.lower() == "n":
            url = resp.get("next")
        elif move.lower() == "p":
            url = resp.get("previous")
        else:
            break
        parsed = urlparse.urlparse(url)
        params["cursor"] = urlparse.parse_qs(parsed.query)["cursor"][0]
        resp = coreapi_client.action(get_document(), keys, params=params)

        echo_resp(resp)


def add_command(parent_command, name, metadata):

    # _type = link denotes a end command, otherwise there is more nested commands to go through
    if metadata.get("_type") == "link":
        options = []

        # fields in coreapi denotes options
        for field in metadata.get("fields", []):
            option_name = "--" + field.get("name")
            options.append(
                click.Option(
                    param_decls=[option_name],
                    prompt=field.get("required", False),
                    help=field.get("schema", {}).get("description", ""),
                )
            )
        command = click.Command(
            name, callback=apicall, help=metadata.get("description", ""), params=options
        )

    else:
        command = click.Group(name, help=metadata.get("description", ""))
        for action, value in metadata.items():
            add_command(command, action, value)
    parent_command.add_command(command)


for action, value in get_raw_document().items():
    if not action.startswith("_"):
        add_command(client, action, value)


if __name__ == "__main__":
    client()
