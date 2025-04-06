import json
import tempfile
import typer
from rich.console import Console
from paxpar.cli.tools import PaxparCLI_ObjCtx, call, root_command_callback
import sys
import yaml
import toml


def version_get():
    return open("VERSION").read().strip()


def pyproject_version_get(target: str):
    """
    get version in a pyproject.toml file
    """
    data = toml.load(open(target))
    return data["project"]["version"]


def pyproject_version_set(
    target: str,
    version: str,
    ctx_obj: PaxparCLI_ObjCtx,
):
    """
    set version in a pyproject.toml file
    """
    try:
        data = toml.load(open(target))
        data["project"]["version"] = version
        if not ctx_obj.dry_run:
            toml.dump(data, open(target, "w"))
        if ctx_obj.verbose:
            print(target + " set to " + version)
    except Exception as e:
        print("Erreur pyproject_version")
        print(e)


def helm_version_set(
    target: str,
    version: str,
    ctx_obj: PaxparCLI_ObjCtx,
):
    """
    set version in a Helm Chart
    """
    # data = yaml.safe_load(open("deploy/paxpar/Chart.yaml"))
    data = yaml.safe_load(open(target))
    data["appVersion"] = version
    data["version"] = version
    if not ctx_obj.dry_run:
        yaml.safe_dump(data, open(target, "w"))
    if ctx_obj.verbose:
        print(f"{target} set to " + version)


console = Console()


def root_command(
    ctx: typer.Context,
):
    if ctx.obj.verbose:
        print(f'pyproject.toml : {pyproject_version_get("pyproject.toml")}')
        print(f'packages/pp-api/pyproject.toml : {pyproject_version_get("packages/pp-api/pyproject.toml")}')
        print(f'packages/pp-cli/pyproject.toml : {pyproject_version_get("packages/pp-cli/pyproject.toml")}')
        print(f'packages/pp-core/pyproject.toml : {pyproject_version_get("packages/pp-core/pyproject.toml")}')
        print(f'packages/pp-schema/pyproject.toml : {pyproject_version_get("packages/pp-schema/pyproject.toml")}')
    else:
        print(version_get())


app = typer.Typer(
    help="Misc pp commands",
    invoke_without_command=True,
    callback=root_command_callback(root_command),
)


@app.command()
def show(
    ctx: typer.Context,
):
    """Show current version (DEFAULT COMMAND)"""
    root_command(ctx)


@app.command()
def bump(
    ctx: typer.Context,
): ...


@app.command()
def set(
    ctx: typer.Context,
    version: str,
):
    ctx_obj: PaxparCLI_ObjCtx = ctx.obj
    # assert len(sys.argv) == 2, "version arg is missing !"
    # version = sys.argv[1].strip()
    if ctx_obj.verbose:
        print(f"set-version to {version} ...")

    # set VERSION file
    if not ctx_obj.dry_run:
        open("VERSION", "w").write(version)
    if ctx_obj.verbose:
        print("VERSION set to " + version)

    # set helm chart version
    helm_version_set("packages/pp-api/deploy/paxpar/Chart.yaml", version, ctx_obj)

    # set pyproject.toml files
    pyproject_version_set("pyproject.toml", version, ctx_obj)
    pyproject_version_set("packages/pp-api/pyproject.toml", version, ctx_obj)
    pyproject_version_set("packages/pp-cli/pyproject.toml", version, ctx_obj)
    pyproject_version_set("packages/pp-core/pyproject.toml", version, ctx_obj)
    pyproject_version_set("packages/pp-schema/pyproject.toml", version, ctx_obj)

    print("set-version done for " + version)
