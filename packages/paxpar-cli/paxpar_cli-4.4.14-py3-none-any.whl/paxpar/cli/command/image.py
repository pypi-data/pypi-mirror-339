import os
import typer
from rich.console import Console

from paxpar.cli.tools import call

console = Console()

app = typer.Typer(help="container image related commands")


REGISTRIES = {
    "gitlab": {
        "url": "registry.gitlab.com",
    },
    "scaleway": {
        "url": "rg.fr-par.scw.cloud/pp-registry-test1",
    },
}


@app.command("list")
def list_command():
    """
    List image registries
    """
    print(REGISTRIES)


@app.command()
def login(
    ctx: typer.Context,
    registry_id: str = "all",
):
    """
    Login to image registry
    """
    registries = list(REGISTRIES.keys()) if registry_id == "all" else [registry_id]

    print("registries", registries)
    for registry_id in registries:
        registry = REGISTRIES[registry_id]
        envv = f"{registry_id.upper()}_SECRET_KEY"
        secret = os.environ[envv]
        cmd = f'''docker login {registry['url']} -u nologin --password-stdin <<< "{secret}"'''

        call(cmd, ctx_obj=ctx.obj)


@app.command()
def pull(
    ctx: typer.Context,
    version: str = "latest",
):
    """
    Start paxpar core service
    """
    registry = REGISTRIES["gitlab"]
    if version[0].isdigit():
        version = f"v{version}"

    cmd=f"""docker pull {registry['url']}/arundo-tech/paxpar/paxpar-core:{version}"""
    call(cmd, ctx_obj=ctx.obj)
