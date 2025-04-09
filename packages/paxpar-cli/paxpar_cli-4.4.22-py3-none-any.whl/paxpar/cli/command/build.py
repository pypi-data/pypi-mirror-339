from typing import Annotated
import typer
from rich.console import Console
from paxpar.cli.tools import call, root_command_callback, PaxparCLI_ObjCtx
from paxpar.cli.command.version import version_get


console = Console()

app = typer.Typer(
    help="Misc pp commands",
    callback=root_command_callback(),
)

@app.command()
def cli(
    ctx: typer.Context,
    uv_publish_token:  Annotated[str, typer.Argument(envvar="UV_PUBLISH_TOKEN")],
    package_publish: bool = True,
):
    '''
    build and publish pp-cli
    '''
    ctx_obj: PaxparCLI_ObjCtx = ctx.obj
    pypi_project_url = "https://pypi.org/project/paxpar-cli/#history"


    # publish pp-cli, pp-schema on pypi
    '''
    [repositories]
    [repositories.gitlab]
    url = "https://gitlab.com/api/v4/projects/32901859/packages/pypi"
    # url = "https://gitlab.com/api/v4/projects/${env.CI_PROJECT_ID}/packages/pypi"
    # cf https://stackoverflow.com/questions/64099010/how-to-deploy-python-packages-to-gitlab-package-registry-with-poetry
    # poetry publish --repository gitlab -u <token-username> -p <token-password>

    #poetry config repositories.gitlab https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/pypi
    #    - poetry config http-basic.gitlab gitlab-ci-token ${CI_JOB_TOKEN}
    '''
    # see https://docs.astral.sh/uv/guides/package/
    call(
        'uv build',
        cwd = 'packages/pp-cli',
        ctx_obj=ctx_obj,
    )

    if package_publish:
        call(
            f'uv publish --token {uv_publish_token}',
            cwd = 'packages/pp-cli',
            ctx_obj=ctx_obj,
        )

        if ctx_obj.verbose:
            #typer.launch(pypi_project_url)
            print(f'See published package at {pypi_project_url}')



@app.command()
def api(
    ctx: typer.Context,

    registry_root:  Annotated[str, typer.Option(envvar="REGISTRY_ROOT")] = "rg.fr-par.scw.cloud",
    registry_prefix:  Annotated[str, typer.Option(envvar="REGISTRY_PREFIX")] = "pp-registry-test1",
    registry_user:  Annotated[str, typer.Option(envvar="REGISTRY_USER")] = "nologin",
    registry_password:  Annotated[str, typer.Option(envvar="REGISTRY_PASSWORD")] = "xxx",

    ci_job_token: Annotated[str, typer.Option(envvar="CI_JOB_TOKEN")] = "xxx",
    ci_api_url: Annotated[str, typer.Option(envvar="CI_API_V4_URL")] = "xxx",
    ci_project_id: Annotated[str, typer.Option(envvar="CI_PROJECT_ID")] = "xxx",

    image_build: bool = True,
    image_publish: bool = True,

    helm_chart_build: bool = True,
    helm_chart_publish: bool = True,

):
    """
    build and publish pp-api
    """
    ctx_obj: PaxparCLI_ObjCtx = ctx.obj

    # see https://pythonspeed.com/articles/gitlab-build-docker-image/
    #VERSION = "0.0.1"
    version = version_get(ctx_obj)

    if ctx_obj.verbose:
        print(f"build API v{version} ...")
        print(f"argument {registry_root=}")
        print(f"argument {registry_prefix=}")
        print(f"argument {registry_user=}")
        print(f"argument {registry_password=}")
        print(f"argument {ci_job_token=}")
        print(f"argument {ci_api_url=}")
        print(f"argument {ci_project_id=}")

    if image_build:
        if image_publish:
            call(
                f'podman login -u "{registry_user}" -p "{registry_password}" "{registry_root}/{registry_prefix}"',
                ctx_obj=ctx_obj,
            )

        call(
            f'podman build -t "{registry_root}/{registry_prefix}/pp-core:{version}" .',
            cwd="packages/pp-api",
            ctx_obj=ctx_obj,
        )
        
        if image_publish:
            call(
                f'podman push "{registry_root}/{registry_prefix}/pp-core:{version}"',
                ctx_obj=ctx_obj,
            )

    if helm_chart_build:
        filename = f"paxpar-{version}.tgz"

        # for some obscur r
        call(f"""
            helm package deploy/paxpar
            mv {filename} ../../
            """,
            cwd="packages/pp-api",
            ctx_obj=ctx_obj,
        )
        print(f"helm chart {filename} built")

        if helm_chart_publish:
            # upload helm chart to gitlab repo
            call(
                f"""
                curl --request POST \
                    --user gitlab-ci-token:{ci_job_token} \
                    --form "chart=@{filename}" \
                    "{ci_api_url}/projects/{ci_project_id}/packages/helm/api/stable/charts"'
                """,
                cwd="packages/pp-api",
                ctx_obj=ctx_obj,
            )
            print(f"helm chart {filename} published")


@app.command()
def front(
    ctx: typer.Context,
):
    """
    build front (bun generate)
    """
    cwd = "packages/pp-front"

    call(
        "npx bun install --frozen-lockfile",
        cwd=cwd,
        ctx_obj=ctx.obj,
    )
    call(
        "npx bun run generate",
        cwd=cwd,
        ctx_obj=ctx.obj,
    )

    call(
        "jupyter lite build --base-url /notebook --output-dir .output/public/notebook/",
        cwd=cwd,
        ctx_obj=ctx.obj,
    )

    # store version in a static /version file
    #- echo "CI_COMMIT_REF_NAME = ${CI_COMMIT_REF_NAME}"
    #- echo "VERSION_RELEASE = ${VERSION_RELEASE}"
    #- echo "${VERSION_RELEASE}" > .output/public/version
    #- echo "{\"version\":\"${VERSION_RELEASE}\",\"role\":\"pp-front\"}" > .output/public/version.json
    # don't create /deploy_conf.json, will be done at deployment time !

    # prepare the artifact
    #- rm -Rf dist
    #- mv .output/public dist


@app.command()
def widgets(
    ctx: typer.Context,
):
    """
    build pp-widgets (bun generate)
    """
    call(
        "npx bun install --frozen-lockfile",
        cwd="packages/pp-widgets",
        ctx_obj=ctx.obj,
    )
    call(
        "npx bun run generate",
        cwd="packages/pp-widgets",
        ctx_obj=ctx.obj,
    )


@app.command()
def all():
    """
    build all ... (NOT IMPLEMENTED)
    """
    raise NotImplementedError()
