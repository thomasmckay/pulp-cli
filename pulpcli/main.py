import click
import click_completion
import coreapi
import json
import urllib.parse as urlparse

from progress.spinner import Spinner
from time import sleep
from uuid import UUID


DOCUMENT_PATH = "/home/vagrant/.coreapi/document.json"
click_completion.init()
decoded_doc = ""

coreapi_client = coreapi.Client()


# Install for click-completion
def install_callback(ctx, attr, value):
    if not value or ctx.resilient_parsing:
        return value
    shell, path = click_completion.install()
    click.echo("%s completion installed in %s" % (shell, path))
    exit(0)


@click.group(invoke_without_command=True)
@click.option(
    "--install",
    is_flag=True,
    callback=install_callback,
    expose_value=False,
    help="Install completion for the current shell. Make sure to have psutil installed.",
)
@click.pass_context
def client(ctx):
    if ctx.invoked_subcommand is not None:
        return
    click.echo(ctx.get_help())


def is_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string


def echo_resp(response):
    codec = coreapi.codecs.DisplayCodec()
    click.secho(codec.encode(response, colorize=True), fg="green")


def apicall(*args, **kwargs):

    ctx = click.get_current_context()
    keys = ctx.command_path.split(" ")[1:]

    params = {k: v for k, v in kwargs.items() if v is not None}

    for k, v in params.items():

        # If as passed in pk is not a uuid, see if we can find the uuid
        if k.endswith("_pk") and not is_uuid4(v):
            resp = coreapi_client.action(
                decoded_doc, [keys[0], "list"], params={"name": v}
            )
            if len(resp["results"]) == 1:
                params[k] = resp["results"][0]["id"]
            else:
                click.secho("Invalid id or name", fg="red")
                return

    resp = coreapi_client.action(decoded_doc, keys, params=params)

    echo_resp(resp)

    # If coreapi client returns task_id, follow it and run a spinner until task is complete
    if "task_id" in resp:
        spinner = Spinner("Loading ")
        task_progress = coreapi_client.action(
            decoded_doc, ["tasks", "read"], params={"id": resp.get("task_id")}
        )
        while task_progress["state"] != "completed":
            spinner.next()
            sleep(.01)
            task_progress = coreapi_client.action(
                decoded_doc, ["tasks", "read"], params={"id": resp.get("task_id")}
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
        resp = coreapi_client.action(decoded_doc, keys, params=params)

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


store = open(DOCUMENT_PATH, "rb")
content = store.read()
store.close()
codec = coreapi.codecs.CoreJSONCodec()
decoded_doc = codec.decode(content)


with open(DOCUMENT_PATH) as doc:
    doc = json.load(doc)
    for action, value in doc.items():
        if not action.startswith("_"):
            add_command(client, action, value)


if __name__ == "__main__":
    client()
